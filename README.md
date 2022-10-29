# Open Assistant

Current development has moved to Gitlab: https://gitlab.com/open-assistant/oa-arch

Open Source Voice Assistant: Make your own minds!

Open Assistant is an offline open source voice assistant prototype able to complete operating system tasks using vocal commands.

## Installation

### macOS

* Install [brew](https://brew.sh/) if you have not already.
* Install pocketsphinx dependencies: `brew install swig openal-soft`
* Link the openal-soft libraries to the include path: `ln -s /usr/local/Cellar/openal-soft/1.20.1/include/AL/* /usr/local/include`
* pip3 install git+https://github.com/Im-Fran/pocketsphinx-python
* Install Python dependencies: `pip3 install -r requirements.txt`

### Ubuntu Linux

* Install system requirements ``sudo apt-get install -y python3 python3-dev python3-pip build-essential swig git libpulse-dev espeak libasound2-dev``
* Install Python dependencies: `pip3 install -r requirements.txt`

### Arch Linux

* Install system requirements ``sudo pacman -S swig espeak``
* Install Python dependencies: `pip install -r requirements.txt`

## Using Open Assistant

* [Download Open Assistant](https://github.com/openassistant/oa-core/archive/master.zip)
* Run Open Assistant from within the unzipped directory: ``python -m oa`` or ``python3 -m oa``
* Make sure your microphone is working and levels are set properly.
* Say "Boot Mind!" as a listening test. If you hear R2D2, boot mind is listening.
* Say "Open Assistant!" to launch root mind. Say "Root Mind!" to see if you can get the reply, "Hello World!"
* Say "List commands!" to get a list of available voice commands.
* Add your own!
