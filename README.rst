Description:
This is fork of original OpenAssistant (see below).
Main goal to simplify and restructure modules to provide easy customization 
and OS independent version of OpenAssistant.
To implement more sofisticated logic like ML (TensorFlow).
OA.Agents network, and customization on fly (adding commands via UI).
Extend UI (now it's only VUI) :
CLI, GUI, AR/VR-UI, BCI, network agents interaction.

This version contains "check for silence delay" similar to SpeechRecognition-3.8.1
Json was replaced with commands.py modules - so it's free to use any logic that you need for Command.

\mind\boot\conf\commands.py
audio.py - all audio logic TTS, STT updates langs from web, etc.
oa.py - main Assistant module
oa_utils.py - Any utilities to simplify Command process. 
there is no auto installer yet. (case it's not Ready2Go version for now).

Removed : gstream, gobject.
------------------------------------------------------------------
Help:
If you want to help in development, you may donate me a cup of coffee. 
(my "core" works better with this stuff =) )

BTC
1HWciwsZ1jCgH9VYRRb4A21WoRByn2tnpc

ETH
0x90A534862fA94FE1fFC1Fe5c660E3683c219c87a

NEO
Ad3FZrL9Gr1WyNcR6GTbPRqgv1c58E2G1q

QTUM
Qd7bqFAGCC5ViHaZqkuYHHo9Jg8h1a1Ugc

DOGE
DMeiGCpCK96xp9g9A1achnB7gYvH6KNc6u

(also accept all tokens, based on corresponded platforms ^^ =) )

------------------------------------------------------------------
NEED to fix:
Need to replace all comands of "minds" via Py Stub calls. 
(to make it work transparently in Win,Mac,Linux and other OS families)
for now it's not complete version (all commands is related to Arch linux)
------------------------------------------------------------------
Installation:
------------------------------------------------------------------
Dependencies:
Python  : 
we suppose it may be any version 2.* or 3.* branch)

Windows
pip install keyboard pyaudio playsound requests pyttsx3 pocketsphinx psutil feedparser
to start: python oa.py

Arch Linux
sudo pacman -S portaudio python-pyaudio swig espeak && sudo pip install keyboard requests pyttsx3 playsound pocketsphinx psutil feedparser
-- still some problems with 
-- ALSA lib pcm.c:2501:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear

Ubuntu
sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev espeak && sudo apt-get install python-pyaudio && sudo pip install keyboard pyttsx3 playsound psutil feedparser
to start: sudo python oa.py

------------------------------------------------------------------
Original:
This fork will be merged with original branch, decision (what part to merge) will be made by OA community.

Open Assistant
=============
Open Assistant is an evolving open source artificial intelligence agent able 
to interact in basic conversation and automate an increasing number of tasks.

Maintained by the `Open Assistant <http://www.openassistant.org/>`__ 
working group lead by `Andrew Vavrek <https://youtu.be/cXqEv2OVwHE>`__, this software 
is an extension of `Blather <https://gitlab.com/jezra/blather>`__ 
by `Jezra <http://www.jezra.net/>`__, `Kaylee <https://github.com/Ratfink/kaylee>`__ 
by `Clayton G. Hobbs <https://bzratfink.wordpress.com/>`__, and includes work 
done by `Jonathan Kulp <http://jonathankulp.org/>`__.
