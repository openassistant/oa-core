# Open Assistant

Open source AI OS development. Make your own minds!

Open Assistant is a private open source personal assistant prototype able to complete tasks using vocal commands.

# Installation

## Windows

Windows (Click & Run)

* Download http://openassistant.org/download/oa_0.21_windows.zip
* Unzip package
* Launch `oa.exe` in "Open Assistant" folder

Windows Python Install (Python 3.x)

* Install [common list of Python packages](https://www.python.org/downloads/windows/)
* Install Windows-specific dependencies: ``pip install pywin32``
* Install Python dependencies: `pip install -r requirements.txt`

## Ubuntu Linux

* Install system requirements ``sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev espeak``
* Install Python dependencies: `pip install -r requirements.txt`

## Arch Linux

* Install system requirements ``sudo pacman -S swig espeak``
* Install Python dependencies: `pip install -r requirements.txt`

# Using Open Assistant

* [Download Open Assistant](https://github.com/openassistant/oa-core/archive/master.zip)
* Run Open Assistant from within the unzipped directory: ``python -m oa``
* Make sure your microphone is working and levels are set properly.
* Say "Boot Mind!" as a listening test. If you hear R2D2, boot mind is listening.
* Say "Open Assistant!" to launch root mind. Say "Root Mind!" to see if you can get the reply, "Hello World!"
* Say "List commands!" to get a list of available voice commands.
