# Open Assistant

Open source AI OS development. Make your own minds! Free the robot brains! Support your privacy and freedom!

Open Assistant is a private open source personal assistant system able to engage in conversations and complete an increasing amount of tasks using vocal commands.

Our current goals are to simplify and restructure modules to provide easy customization, operating system independence, as well as to implement more sophisticated logic such as machine learning (TensorFlow).

We would like to establish an OA.Agents blockchain network, add the ability for customization on fly (adding or changing commands via voice), provide a graphical interface, and build auto installer scripts.

# Video Demonstrations

* [First run on Arch Linux](https://youtu.be/-7Vh1ny9FsQ)
* [Version 0.11 on Arch Linux](https://youtu.be/_zBjn_LgiZM)
* [First run on Windows](https://youtu.be/6_tA081SA8Y)
* [Short Calculator Demonstration](https://youtu.be/ueQCmmUdmLo)
* [German Language Demonstration](https://youtu.be/ElWUBI2e5Mg)

# Getting Started

* [Download Open Assistant](https://github.com/openassistant/oa-core/archive/master.zip)
* Run Open Assistant ``python oa.py``

## General

``pip install keyboard sounddevice playsound requests pyttsx3 pocketsphinx psutil feedparser python-forecastio numpy``

## Windows

Windows (Click & Run)

* Download http://openassistant.org/download/oa_0.21_windows.zip
* Unzip package
* Launch `oa.exe` in "Open Assistant" folder

Windows Python Install (Python 3.x)

* Install [common list of Python packages](https://www.python.org/downloads/windows/)
* Install Windows-specific dependencies ``pip install pywin32``
* Install OA dependencies (see General)

## Ubuntu Linux

* Install system requirements ``sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev espeak``
* Install Python dependencies (see General)

## Arch Linux

* Install system requirements ``sudo pacman -S swig espeak``
* Install Python dependencies (see General)

# Using Open Assistant

* Make sure your microphone is working and levels are set properly.
* Say "Boot mind!" as a listening test. If you hear R2D2, boot mind is listening.
* Say "Open assistant!" to launch root mind. Say "Root mind!" to see if you can get the reply, "Hello world!"
* Say "List commands!" to get a list of available voice commands.
