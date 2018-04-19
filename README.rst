Open Assistant Fork Description:
=============

This is fork of the original `Open Assistant <http://www.openassistant.org/>`__ (see below).

Our goals are to simplify and restructure modules to provide easy customization, operating system independence, as well as to implement more sophisticated logic such as machine learning (TensorFlow).

We would like to establish an OA.Agents blockchain network, add the ability for customization on fly (adding or changing commands via voice), provide a graphical interface, and build auto installer scripts.

This version contains a "check for silence delay" similar to  `SpeechRecognition-3.8.1 <https://pypi.python.org/pypi/SpeechRecognition/3.8.1>`__.

JSON was replaced with ``commands.py`` modules, so this frees up any logic needed for commands.

``\mind\boot\conf\commands.py`` - Main commands file (boot mind).

``audio.py`` - Audio logic TTS, STT, and updates language files from web.

``oa.py`` - Main Assistant module.

``oa_utils.py`` - Utilities to simplify command processes.

Demo : 
=============
first run on win
https://www.youtube.com/watch?v=6_tA081SA8Y

small calc demo:
https://www.youtube.com/watch?v=ueQCmmUdmLo

Need To Fix:
=============
Replace all commands in "minds" via Python Stub calls. 

Make OA work transparently in Windows, Mac, Linux and all other OS families (all commands are currently related to Arch linux).

Installation:
=============
Dependencies:

Python: (May be any version 2.* or 3.* branch.)

Windows:

``pip install keyboard sounddevice playsound requests pyttsx3 pocketsphinx psutil feedparser python-forecastio``
to start: ``python oa.py``

Arch Linux:

``sudo pacman -S swig espeak && sudo pip install sounddevice playsound keyboard requests pyttsx3 pocketsphinx psutil feedparser python-forecastio``

Ubuntu:

``sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev espeak && sudo pip install sounddevice playsound keyboard pyttsx3 psutil feedparser python-forecastio``

To start: ``sudo python oa.py``

Help:
=============
If you want to help support this development, you may donate a cup of coffee. (My "core" works better with this stuff =) )

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

(All tokens are accepted, based on corresponded platforms ^^ =) )

Original:
=============
This fork will be merged with original branch, decision (what part to merge) will be made by OA community.

Open Assistant
=============
Open Assistant is an evolving open source artificial intelligence agent able  to interact in basic conversation and automate an increasing number of tasks.

Maintained by the `Open Assistant <http://www.openassistant.org/>`__ 
working group lead by `Andrew Vavrek <https://youtu.be/cXqEv2OVwHE>`__, this software 
is an extension of `Blather <https://gitlab.com/jezra/blather>`__ 
by `Jezra <http://www.jezra.net/>`__, `Kaylee <https://github.com/Ratfink/kaylee>`__ 
by `Clayton G. Hobbs <https://bzratfink.wordpress.com/>`__, and includes work 
done by `Jonathan Kulp <http://jonathankulp.org/>`__.
