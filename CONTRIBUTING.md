# Design Information

[General Open Assistant overview](http://openassistant.org/wp/)

## Core

* ``oa.py`` - Main Open Assistant loading module.
* ``core.py`` - Essential functions and utilities. This also contains additional functions to play sounds, run diagnostics, report the weather, and read the news. (These functions will eventually be split into individual 'ability files'). Look within 'minds/root.py' for various voice command examples.

## Minds

* ``boot.py`` - First mind booted. Listens for "open assistant" vocal command to launch ``root.py``.
* ``root.py`` - Core system mind (will be configured specifically for various operating systems).
 
## Parts

* ``console.py`` - Display messages in the console.
* ``display.py`` - Show messages/windows/dialogs/video in Python web browser (under development).
* ``ear.py`` - Listening to audio via microphone.
* ``eye.py`` - Camera and computer vision (planned).
* ``keyboard.py`` - Recieve keyboard keys/emulate keyboard keys from input queue (`wire_in`).
* ``sound.py`` - Play audio file via speakers.
* ``stt.py`` - Internal speech to text.
* ``voice.py`` - Text to speech via speakers.
* ``mind.py``  - Load and control all minds.
  
  About parts:
    ``_in()`` - function which `yields` processed data. Each part works in a separate thread.
    
    Each part reads messages (signals) from devices and/or from an input message wire (``wire_in``).
    
    To send messages to a part ('voice' for example) use: ``put('voice','any sentence')``
    To read messages (for current part) use: ``data = get()`` (get waits until any messages appear on the wire).
    
    In sophisticated cases you may use ``wire_in`` directly (with or without locks).
    
    Newly added parts will start automatically.

	  
# To-Do List
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


 # Support Open Assistant

[Become a patron](https://www.patreon.com/openassistant)

Donate tokens
 
BTC: 1HWciwsZ1jCgH9VYRRb4A21WoRByn2tnpc

ETH: 0x90A534862fA94FE1fFC1Fe5c660E3683c219c87a

NEO: Ad3FZrL9Gr1WyNcR6GTbPRqgv1c58E2G1q

QTUM: Qd7bqFAGCC5ViHaZqkuYHHo9Jg8h1a1Ugc

DOGE: DMeiGCpCK96xp9g9A1achnB7gYvH6KNc6u

MANNA: GLfvi9GWmRQdpeN8nDdjMkbCjvk55viTXp

# Join the Team

Feel free to fork and enhance this code!

Email us at info@openassistant.org

[Visit our website](http://www.openassistant.org)