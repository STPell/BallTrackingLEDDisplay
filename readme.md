# Motion Tracking Feature Wall

This repo contains the software for a prototype version of a Motion Tracking Feature Wall. The prototype version only tracks a green ball using a python program which communicates the position, speed, and angle of movement to the LED controller.

The two separate versions of the LED controller are included in ``arduino_led_controller`` and ``backup-board``. Ball tracking software is in ``python_ball_tracker``. More information on each of the modules is included below.

## Motion Tracking.
_Written by Samuel Pell (@spe80)_

The software developed for the prototype runs in python and uses the OpenCV library. Currently, it only tracks a single green object at a time and is sensitive to light conditions - the bare minimum required to demonstrate functionality.

### Installing the code to run the python ball tracking software.

The python code requires the following external libraries,
* ``numpy``
* ``imutils``
* `OpenCV`
* ``pyserial``
	
To install these on windows the following script is used.
```
pip install numpy imutils pyserial
pip install opencv-contrib-python
```

To install this on unices similar commands can be used after pip is installed. 

### Serial communication

Serial communication is performed using the ``pyserial`` library wrapped in a multithreaded SerialController class. The clase uses a baud rate of 9600 and sends UTF8 encoded comma separated values terminated by a new line. To change which internal port the class connects to change line 177 in ``end_deliverable.py``.


### Running the program

``python3 end_deliverable.py [options]``

There are five possible options:
* ``-v video_path`` specifies a video file to pull data from. This cannot be used in conjuction with the ``-c`` flag and will overide it.
* ``-c [camera id]`` specifies to use a specific camera. Camera id's can be found via trial and error, consulting the OS, and defaults to 0 (typically the only camera attached or the built in webcam).
* ``-s`` specifies serial output is to be generated and sent.
* ``-pc`` specifies that the serial output should also be printed to console.
* ``-d`` displays the camera's view and diagnostic markers on screen. To gracefully close the program the key 'q' can be pressed in this mode to exit the program.
	
## LED Controller.
_Written by Ash Gupta (@agu50)_

Two versions of the LED program exists for different array sizes. The one used to demonstrate the prototype was ``backup-board``. The LED controller was an Arduino UNO board controlling individually addressable RGB LEDs in a 9x10 grid. 

Four different modes exits: standby, piano, game, and draw. These modes can be toggled via a swich connected to pin 10.
	