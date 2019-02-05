# ear.py - Speech recognition input.

import collections
import math

import audioop
import numpy
import sounddevice

from oa.core import oa

DEFAULT_CONFIG = {
    # The `timeout` parameter is the maximum number of seconds that a phrase continues before stopping and returning a result. If the `timeout` is None there will be no phrase time limit.
    "timeout": None,

    "channels": 1,

    # Sampling rate in Hertz
    "sample_rate": 16000,

    # size of each sample
    "sample_width": 2,

    # Number of frames stored in each buffer.
    "chunk": 1024,

    # Minimum audio energy to consider for recording.
    "energy_threshold": 300,

    "dynamic_energy_threshold": False,
    "dynamic_energy_adjustment_damping": 0.15,
    "dynamic_energy_ratio": 1.5,

    # Seconds of non-speaking audio before a phrase is considered complete.
    "pause_threshold": 0.8,

    # Minimum seconds of speaking audio before we consider the audio a phrase - values below this are ignored (for filtering out clicks and pops).
    "phrase_threshold": 0.3,

    # Maximum number of seconds that a phrase continues before stopping and returning a result. If the `timeout` is None there will be no phrase time limit.
    "phrase_time_limit": 5,

    # Seconds of non-speaking audio to keep on both sides of the recording.
    "non_speaking_duration": 0.8,
}

def init():
    print("hello")

def _in(ctx):
    _config = DEFAULT_CONFIG.copy()

    seconds_per_buffer = _config.get("chunk") / _config.get("sample_rate")
    pause_buffer_count = math.ceil(_config.get("pause_threshold") / seconds_per_buffer)

    # Number of buffers of non-speaking audio during a phrase before the phrase should be considered complete.
    phrase_buffer_count = math.ceil(_config.get("phrase_threshold") / seconds_per_buffer) # Minimum number of buffers of speaking audio before we consider the speaking audio a phrase.
    non_speaking_buffer_count = math.ceil(_config.get("non_speaking_duration") / seconds_per_buffer)  # Maximum number of buffers of non-speaking audio to retain before and after a phrase.
    stream = sounddevice.Stream(samplerate=_config.get("sample_rate"), channels=_config.get("channels"), dtype='int16')
    with stream:
        while not ctx.finished.is_set():
            elapsed_time = 0  # Number of seconds of audio read
            buf = b""  # An empty buffer means that the stream has ended and there is no data left to read.
            while not ctx.finished.is_set():
                frames = collections.deque()

                # Store audio input until the phrase starts
                while not ctx.finished.is_set():
                    # Handle waiting too long for phrase by raising an exception
                    elapsed_time += seconds_per_buffer
                    if _config.get("timeout") and (elapsed_time > _config.get("timeout")):
                        raise Exception("Listening timed out while waiting for phrase to start.")

                    buf = stream.read(_config.get("chunk"))[0]
                    frames.append(buf)
                    if len(frames) > non_speaking_buffer_count:  
                    # Ensure we only keep the required amount of non-speaking buffers.
                        frames.popleft()

                    # Detect whether speaking has started on audio input.
                    energy = audioop.rms(buf, _config.get("sample_width"))  # Energy of the audio signal.
                    if energy > _config.get("energy_threshold"):
                        break

                    # Dynamically adjust the energy threshold using asymmetric weighted average.
                    if _config.get("dynamic_energy_threshold"):
                        damping = _config.get("dynamic_energy_adjustment_damping") ** seconds_per_buffer  # Account for different chunk sizes and rates.
                        target_energy = energy * _config.get("dynamic_energy_ratio")
                        _config["energy_threshold"] = _config.get("energy_threshold") * damping + target_energy * (1 - damping)

                # Read audio input until the phrase ends.
                pause_count, phrase_count = 0, 0
                phrase_start_time = elapsed_time
                while not ctx.finished.is_set():
                    # Handle phrase being too long by cutting off the audio.
                    elapsed_time += seconds_per_buffer
                    if _config.get("phrase_time_limit") and elapsed_time - phrase_start_time > _config.get("phrase_time_limit"):
                        break

                    buf = stream.read(_config.get("chunk"))[0]
                    frames.append(buf)
                    phrase_count += 1

                    # Check if speaking has stopped for longer than the pause threshold on the audio input.
                    energy = audioop.rms(buf, _config.get("sample_width"))  # unit energy of the audio signal within the buffer.
                    if energy > _config.get("energy_threshold"):
                        pause_count = 0
                    else:
                        pause_count += 1
                    if pause_count > pause_buffer_count:  # End of the phrase.
                        break

                # Check how long the detected phrase is and retry listening if the phrase is too short.
                phrase_count -= pause_count  # Exclude the buffers for the pause before the phrase.
                if phrase_count >= phrase_buffer_count or len(buf) == 0: break  # Phrase is long enough or we've reached the end of the stream, so stop listening.

            # Obtain frame data.
            for _ in range(pause_count - non_speaking_buffer_count): frames.pop()  # Remove extra non-speaking frames at the end.
            frame_data = numpy.concatenate(frames)
            yield frame_data