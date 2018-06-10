Open Assistant
==============

Make your own minds! Open source AI OS development.

Open Assistant is a private open source personal assistant system able to engage in conversations and complete an increasing amount of tasks using vocal commands.

Our current goals are to simplify and restructure modules to provide easy customization, operating system independence, as well as to implement more sophisticated logic such as machine learning (TensorFlow).

We would like to establish an OA.Agents blockchain network, add the ability for customization on fly (adding or changing commands via voice), provide a graphical interface, and build auto installer scripts.

Video Demonstrations: 
=============
First run on Arch Linux: 
 https://youtu.be/-7Vh1ny9FsQ

Version 0.11 on Arch Linux: 
 https://youtu.be/_zBjn_LgiZM

First run on Windows: 
 https://youtu.be/6_tA081SA8Y

Short Calculator Demonstration: 
 https://youtu.be/ueQCmmUdmLo

German Language Demonstration: 
 https://youtu.be/ElWUBI2e5Mg

Download, Install, & Run:
=============

`Windows (Click & Run)`:
  `Download <http://openassistant.org/download/oa_0.21_windows.zip>`__, `unzip package <http://www.peazip.org>`__, and click the ``oa.exe`` file found in the "Open Assistant" folder.

`Windows Python Install (Python 2.7 or 3.5 Recommended):
 `Install common list of Python packages <https://www.python.org/downloads/windows/>`__ then run: 
  
 ``pip install pywin32 keyboard sounddevice playsound requests pyttsx3 pocketsphinx psutil feedparser python-forecastio numpy``

`Ubuntu Linux`: 
  ``sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev espeak``
  
  ``pip install keyboard sounddevice playsound requests pyttsx3 pocketsphinx psutil feedparser python-forecastio numpy``

`Arch Linux`: 
  ``sudo pacman -S swig espeak``
  
  ``pip install keyboard sounddevice playsound requests pyttsx3 pocketsphinx psutil feedparser python-forecastio numpy``

`Download Open Assistant`:
  https://github.com/openassistant/oa-core/archive/next.zip

`Run Open Assistant`: 
  ``sudo python oa.py``

Using Open Assistant
=============

Make sure your microphone is working and levels are set properly.

Say "Boot mind!" as a listening test. If you hear R2D2, boot mind is listening.

Say "Open assistant!" to launch root mind. Say "Root mind!" to see if you can get the reply, "Hello world!"

Say "List commands!" to get a list of available voice commands.

System Information:
=============
General Open Assistant overview:
 http://openassistant.org/wp/

``oa.py`` - Main Open Assistant loading module.

``core.py`` - Essential functions and utilities. This also contains additional functions to play sounds, run diagnostics, report the weather, and read the news. (These functions will eventually be split into individual 'ability files'). Look within 'minds/root.py' for various voice command examples.

`Minds`:
  ``boot.py`` - First mind booted. Listens for "open assistant" vocal command to launch ``root.py``.
      
  ``root.py`` - Core system mind (will be configured specifically for various operating systems).
 
`Parts`:
  ``console.py`` - Display messages in the console.
  
  ``display.py`` - Show messages/windows/dialogs/video in Python web browser (under development).
  
  ``ear.py`` - Listening to audio via microphone.
  
  ``eye.py`` - Camera and computer vision (planned).
  
  ``keyboard.py`` - Recieve keyboard keys/emulate keyboard keys from input queue (`wire_in`).
  
  ``sound.py`` - Play audio file via speakers.
  
  ``stt.py`` - Internal speech to text.
  
  ``voice.py`` - Text to speech via speakers.
  
  ``mind.py``  - Load and control all minds.
  
  About parts:
    ``_in()`` - function which `yields` processed data. Each part works in a separate thread.
    
    Each part reads messages (signals) from devices and/or from an input message wire (``wire_in``).
    
    To send messages to a part ('voice' for example) use: ``put('voice','any sentence')``
    To read messages (for current part) use: ``data = get()`` (get waits until any messages appear on the wire).
    
    In sophisticated cases you may use ``wire_in`` directly (with or without locks).
    
    Newly added parts will start automatically.

	  
To-Do List:
=============
Develop further abilities and minds.

Improve speech recogition and voice synthesis.

Make OA work transparently in Windows, Mac, Linux, and all other operating systems.

Display.py (use embedded browser as a display).

 Messages / windows / dialogs / video / input / search / database browser.
  
 Using embedded chromium: https://github.com/cztomczak/cefpython
	
Keyboard command input.

Add new commands via voice (extend mind functionality on fly).

Eye tracking system (mouse control via eyes and video camera):

 https://github.com/esdalmaijer/webcam-eyetracker
 
 https://github.com/esdalmaijer/PyGaze
 
 https://github.com/pupil-labs/pupil

Emotional interaction / lip reading (advanced functionality):

 https://github.com/deepconvolution/LipNet
 
 https://github.com/rizkiarm/LipNet

3D object creation via voice using programmable Openscad:

 https://github.com/SolidCode/SolidPython

Build a simple installer for all operating systems via PyInstaller:

 http://www.pyinstaller.org
      
Support Open Assistant
=============
`Become a patron`:
  https://www.patreon.com/openassistant

`Donate tokens`:
 BTC: 1HWciwsZ1jCgH9VYRRb4A21WoRByn2tnpc
  
 ETH: 0x90A534862fA94FE1fFC1Fe5c660E3683c219c87a
  
 NEO: Ad3FZrL9Gr1WyNcR6GTbPRqgv1c58E2G1q
  
 QTUM: Qd7bqFAGCC5ViHaZqkuYHHo9Jg8h1a1Ugc
  
 DOGE: DMeiGCpCK96xp9g9A1achnB7gYvH6KNc6u
  
 MANNA: GLfvi9GWmRQdpeN8nDdjMkbCjvk55viTXp

Join Our Team
=============
Feel free to fork and enhance this code!

Email us at:
 `info@openassistant.org <mailto:info@openassistant.org>`__

Visit our website:
 http://www.openassistant.org

Free the robot brains!
=============

Support your privacy and freedom!
=============
