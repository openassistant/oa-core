Open Assistant
=============

Make your own minds! Free open source AI OS development.

This is fork of the original `Open Assistant https://github.com/openassistant/oa-core/>`__.

Our goals are to simplify and restructure modules to provide easy customization, operating system independence, as well as to implement more sophisticated logic such as machine learning (TensorFlow).

We would like to establish an OA.Agents blockchain network, add the ability for customization on fly (adding or changing commands via voice), provide a graphical interface, and build auto installer scripts.

Video Demonstrations: 
=============
First run on Arch Linux: https://youtu.be/-7Vh1ny9FsQ

Version 0.11 on Arch Linux: https://youtu.be/_zBjn_LgiZM

First run on Windows: https://www.youtube.com/watch?v=6_tA081SA8Y

Short caculator demo: https://www.youtube.com/watch?v=ueQCmmUdmLo

Installation:
=============
`Dependencies`:

Python: (May be any version 2.* or 3.* branch.)

For all systems: ``pip install keyboard sounddevice playsound requests pyttsx3 pocketsphinx psutil feedparser python-forecastio numpy``

`Windows` (recommended : Python 2.7 or 3.5):

  Install common list of py packages plus: ``pip install pywin32``

  To start Open Assistant: ``python oa.py``

`Arch Linux`: ``sudo pacman -S swig espeak``

`Ubuntu`: ``sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev espeak``

To start Open Assistant: ``sudo python oa.py``

System Information:
=============
General Open Assistant overview: https://www.patreon.com/posts/open-assistant-16695777

`oa.py` - Main Open Assistant module.
  /part - Part modules. 
    ``_in()``: function which `yields` processed data.
    Each part works in separate thread. 
    Each part reads messages (signals) from devices and/or from input message queue (q_in).
    To send messages to a part ('voice' for example) use : put('voice','any sentence')
    To read messages (for current part) use: ``data=get()`` #get waits until any messages appear in the queue.
    In sophisticated cases you may use ``q_in`` queue directly (with or without locks).
    Newly added parts will start automatically.

`oa_utils.py`
  Collection of utilities to play sounds, find files, and execute functions.
  Automatically loaded into each `mind` space (with auto-delayed execution stubs).
  Look within any `mind` for examples.

`Listeners`:  Parts able to receive messages.

  `oa.ear.subs=[oa.stt] (speech to text will receive message from ear).`
  
  `oa.stt.subs=[oa.mind] ...`
  
  `oa.keyb.subs=[oa.mind,oa.display]`

`Parts`:
  `console.py` - Display messages in the console.
  
  `display.py` - Display messages/windows/dialogs/video in py automated web browser (under development).
  
  `ear.py` - Listening via microphone.
  
  `eye.py` - Camera and computer vision (planned).
  
  `keybd.py` - Recieve keyboard keys/emulate keyboard keys from input queue (q_in).
  
  `sound.py` - Play audio file.
  
  `stt.py` - Speech to text.
  
  `voice.py` - Text to speech.
  
  `mind.py`  - Load and control all minds.
  
`Minds`:
    
   `boot.py` - First mind booted. Listens for ``open assistant`` to launch root mind.
       
   `calc.py` - Voice calculator.
       
   `empty.py` - Test mind.
       
   `root.py` - Core system mind (will be configured for various operating systems).
       
   `stella.py` - User mind to talk, get news, hear jokes, and so on.
       
    yes_no.py` - Mind which offers voice options. (You may test this mind via stella ->"How Are you ?" to start diagnostics.)
	  
TO-DO List:
=============
  Clean commands in "minds". 

  Make OA work transparently in Windows, Mac, Linux, and all other operating systems.

  Display.py (use embedded browser as a display)

	messages/windows/dialogs/video/input/search/db browser.
	
	embedded chromium (https://github.com/cztomczak/cefpython)
	
  Keyboard command input.

  Add new commands via voice (extend mind functionality on fly).

  Eye tracking system (mouse with eyes and webcam):

    https://github.com/esdalmaijer/webcam-eyetracker
  
    https://github.com/esdalmaijer/PyGaze
  
    https://github.com/pupil-labs/pupil

  Emotions interaction / Lip syncing (advanced interactions):

    https://github.com/deepconvolution/LipNet
  
    https://github.com/rizkiarm/LipNet

  3D object creation via voice using programmable Openscad: 

    https://github.com/SolidCode/SolidPython

  Build an installer (for all operating systems via PyInstaller).
      
Support Open Assistant:
=============
  Become a patron: https://www.patreon.com/openassistant

  Donate tokens:

    BTC: 1HWciwsZ1jCgH9VYRRb4A21WoRByn2tnpc

    ETH: 0x90A534862fA94FE1fFC1Fe5c660E3683c219c87a

    NEO: Ad3FZrL9Gr1WyNcR6GTbPRqgv1c58E2G1q

    QTUM: Qd7bqFAGCC5ViHaZqkuYHHo9Jg8h1a1Ugc

    DOGE: DMeiGCpCK96xp9g9A1achnB7gYvH6KNc6u

    MANNA: GLfvi9GWmRQdpeN8nDdjMkbCjvk55viTXp

  Join our team:

    Feel free to fork and enhance this project.

    Email us at: `info@openassistant.org <mailto:info@openassistant.org>`__

    Visit our website: `Open Assistant <http://www.openassistant.org/>`__

`Free the robot brains!` 

`Support your privacy and freedom.`
