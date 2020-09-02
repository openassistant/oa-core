# Design Information

[General Open Assistant overview](http://openassistant.org/)

## Bootstrap Process

`oa.__main__.py` bootstraps the system. Responsible for loading config, setting up logging,
and starting up the hub and legacy stacks...

A call to a start() function within `oa.__main__.py` imports a command_loop function, then
`oa.core.hub::run()` is kicked off.

`oa.core.hub::run()` clears the thread finished flag, loads the modules listed in the "modules"
configuration item passed over from the config by calling `oa.core.hub::_load_modules()`, which
is a wrapper for `oa.core.util::load_module()`, passing the module path. Instantiated module
objects are then stored in the `hub.parts` dictionary with the module name as the key.

After the modules are instantiated and stored, `oa.core.hub::_start_modules()` iterates through
the list of modules to instantiate thread barriers and module threads, then starts them using
the `oa.core.hub::thread_loop()` function, passing itself, the module, and the thread barrier.

`oa.core.hub::thread_loop()` calls the module initialization method, if it exists, and then
each thread loops waiting to hear for messages from it's upstream resource.

From there, the `oa.modules.mind` module is the last to load if the system is respecting config
order. boot and root minds are loaded sequentially, and the system is readied.

## System Parts

### Core

| Part | Description |
| ---- | ----------- |
| Hub | Currently the backbone of the system. Runs in the main thread and manages the child threads containing the loaded modules. Responsible for bootstrapping each module and wiring up each for input and output. |
| Agent | Does not appear to be currently used. Looks to be an early version of Hub. |
| Util | Holds the code for the command registry and module loading. |


### Modules

``_in()`` - function which `yields` processed data. Each part works in a separate thread.

Each part reads messages (signals) from devices and/or from an input message wire (``wire_in``).

To send messages to a part ('voice' for example) use: ``put('voice','any sentence')``
To read messages (for current part) use: ``data = get()`` (get waits until any messages appear on the wire).

In sophisticated cases you may use ``wire_in`` directly (with or without locks).

Newly added parts will start automatically.

| Part | Description | 
| ---- | ----------- |
| abilities | The abilities module contains functional code that is called by other modules to complete tasks requested of it via voice or text command with the exception of the `core.py` file. `core.py` appears responsible for handling some of the communications between modules and thread management. |
| ear | Responsible for taking audio from the local sound device and converting it to frame data to be passed downstream. All functionality is fired through `__init__.py::in()`. |
| mind | Contains the boot and root minds, which define commands to add to the command registry. Each mind has it's own set of commands. Root mind used to come online after voice command, but now comes up automatically as part of boot strapping. Boot mind commands are focused on low level system functions such as listing commands and shutting the system down, where root mind is responsible for all the other commands. |
| sound | Plays sounds files to the audio output bus via the playsound library. |
| speech_recognition | Takes frame data from ear and works to decode what was said. |
| voice | Text to speech via speakers. Contains an incoming channel that listens to the bus, using pyttsx3 to output. |

---

## To-Do List

Our current goals are to simplify and restructure modules to provide easy customization, operating system independence, as well as to implement more sophisticated logic such as machine learning (TensorFlow).

We would like to establish an OA.Agents blockchain network, add the ability for customization on fly (adding or changing commands via voice), provide a graphical interface, and build auto installer scripts.

1. Develop further abilities and minds.
1. Improve speech recogition and voice synthesis.
1. Make OA work transparently in Windows, Mac, Linux, and all other operating systems.
1. Display.py (use embedded browser as a display).
    * Messages / windows / dialogs / video / input / search / database browser.
    * Using embedded chromium: [https://github.com/cztomczak/cefpython](https://github.com/cztomczak/cefpython)
1. ~~Keyboard command input.~~
1. Add new commands via voice (extend mind functionality on fly).
1. Eye tracking system (mouse control via eyes and video camera):
    * [https://github.com/esdalmaijer/webcam-eyetracker](https://github.com/esdalmaijer/webcam-eyetracker)
    * [https://github.com/esdalmaijer/PyGaze](https://github.com/esdalmaijer/PyGaze)
    * [https://github.com/pupil-labs/pupil](https://github.com/pupil-labs/pupil)
1. Emotional interaction / lip reading (advanced functionality):
    * [https://github.com/deepconvolution/LipNet](https://github.com/deepconvolution/LipNet)
    * [https://github.com/rizkiarm/LipNet](https://github.com/rizkiarm/LipNet)
1. 3D object creation via voice using programmable Openscad:
    * [https://github.com/SolidCode/SolidPython](https://github.com/SolidCode/SolidPython)
1. Build a simple installer for all operating systems via PyInstaller:
    * [http://www.pyinstaller.org](http://www.pyinstaller.org)
1. Standardize language for module/part throughout the codebase.
1. Simplify Core.Hub and Core.Util functionality to move module loading into the hub so that it can handle it's own stuff.
1. Consider making the command registry a singleton or some sort of OOP pattern so that it can be more modular.
1. Consider a dependency injection model for module/part loading.
1. Verify that keyboard command input is working.
1. Begin writing unit testing.

---

## Join the Team

Feel free to fork and enhance this code!

Email us at info@openassistant.org

[Visit our website](http://www.openassistant.org)
