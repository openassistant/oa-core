Open Assistant Fork Description:
=============

This is fork of the original `Open Assistant <http://www.openassistant.org/>`__ (see below).

Our goals are to simplify and restructure modules to provide easy customization, operating system independence, as well as to implement more sophisticated logic such as machine learning (TensorFlow).

We would like to establish an OA.Agents blockchain network, add the ability for customization on fly (adding or changing commands via voice), provide a graphical interface, and build auto installer scripts.

For additional technical information please take a look at Development section.

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

Windows (recommended : python 2.7 or 3.5):

please install common list of py packages plus:
pip install pywin32

to start: ``python oa.py``

Arch Linux:
``sudo pacman -S swig espeak``

Ubuntu:
``sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev espeak``

To start: ``sudo python oa.py``

for all systems:
``pip install keyboard sounddevice playsound requests pyttsx3 pocketsphinx psutil feedparser python-forecastio numpy``

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

Development:
=============
`oa.py` - main Open Assistant module
  /part - part modules. 
    Please define _in(): function which will `yield` processed data.
    each part works in separate thread. 
    each part may read messages (signals) from devices and/or from input messages Queue. (q_in)
    to send message to some Part ('voice' for example) please use : put('voice','Any sentence')
    to read message (for current part) use : data=get() #get wait until any message appear in Queue.
    in sophisticated causes you may use `q_in` - Queue - directly. (with or without locks).
    you may add a new part and it will start automatically.

`oa_utils.py`
  set of utils to play sound, find and execute files and so on.
  automatically loaded into each `mind` space (with auto-delayed execution stubs).
  please take a look on any `mind` for example.

Subscribers (defined in oa.py - for now):
#subscribers- listeners will receive message from part
  oa.ear.subs=[oa.stt] (speech to text will receive message from ear)
  oa.stt.subs=[oa.mind] ...
  oa.keyb.subs=[oa.mind,oa.display]

parts:
  `console.py` - display messages in console.
  `display.py` - display messages in py automated web browser. (in development)
               embedded chromium (https://github.com/cztomczak/cefpython)
  `ear.py` - listen mic
  `eye.py` - web camera
  `keybd.py` - get keyboard keys/emulate keyboard keys from Input Queue (q_in)
  `sound.py` - play audio file
  `stt.py` - speech to text
  `voice.py` - text to speech
  `mind.py`  - load and control all minds
    \mind
       `boot.py` - main loader
       `calc.py` - voice calculator 
       `empty.py` - tests
       `root_arch.py` - basic system config (will be used for different OSes too).
       `stella.py` - mind to talk, get news, jokes and so on.
       `yes_no.py` - mind which let choose user voice option. 
          (you may test it via stella->"How Are you ?" to start diagnostic)
      
Open Assistant
=============
Open Assistant is an evolving open source artificial intelligence agent able  to interact in basic conversation and automate an increasing number of tasks.

Maintained by the `Open Assistant <http://www.openassistant.org/>`__ 
working group lead by `Andrew Vavrek <https://youtu.be/cXqEv2OVwHE>`__, this software 
is an extension of `Blather <https://gitlab.com/jezra/blather>`__ 
by `Jezra <http://www.jezra.net/>`__, `Kaylee <https://github.com/Ratfink/kaylee>`__ 
by `Clayton G. Hobbs <https://bzratfink.wordpress.com/>`__, and includes work 
done by `Jonathan Kulp <http://jonathankulp.org/>`__.
