[![Python application](https://github.com/BUSH222/pioneer-mini-controller/actions/workflows/python-app.yml/badge.svg)](https://github.com/BUSH222/pioneer-mini-controller/actions/workflows/python-app.yml)

# Pioneer mini controller
This repository contains a program to control geoscan's pioneer mini drone, written im python using dearpygui.


## Table of Contents
- [Features](#features)
- [Installation Instructions](#installation-instructions)
- [How to Use](#how-to-use)
  - [Connection](#connection)
  - [Arm Your Drone's Propellers](#arm-your-drones-propellers)
  - [Take Off](#take-off)
  - [Taking Videos/Photos Mid-Flight](#taking-videosphotos-mid-flight)
  - [LED Control](#led-control)
  - [UI Control](#ui-control)
  - [Script Control](#script-control)
  - [Navbar](#navbar)
- [Code Structure](#code-structure)
  - [Core](#core)
  - [UI](#ui)
  - [main.py](#mainpy)
  - [misc](#misc)
- [Contributing Guidelines](#contributing-guidelines)
  - [Reporting Issues](#reporting-issues)
  - [Submitting Pull Requests](#submitting-pull-requests)
  - [Coding Standards](#coding-standards)
- [License](#license)
## Features

- **Drone Connection**: Connect to the Pioneer Mini drone and monitor its status.
- **Camera Integration**: Connect to the drone's camera, take pictures, and record videos.
- **Manual and Stabilized Control Modes**: Switch between manual and stabilized control modes for precise drone operation.
- **LED Control**: Customize the drone's LED colors.
- **Keyboard Input**: Use keyboard shortcuts to control the drone's throttle, pitch, roll, and yaw.
- **Graphical Interface**: Intuitive UI for managing drone and camera settings.

## Installation Instructions:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/BUSH222/pioneer-mini-controller.git
    cd pioneer-mini-controller
    ```

2. **Set Up a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip3 install -r requirements.txt  # On Windows: pip
    ```

4. **Run the Application**:
    ```bash
    python3 main.py  # On Windows: python
    ```

5. **Additional Notes**:
    - Ensure Python 3.8 or higher is installed on your system.
    - Make sure you have the necessary permissions to connect to the drone's network.



## How to use:
When you run the application, this window should appear:
![Alt text](/misc/readme_images/1.png "UI")

Before launching the application, ensure that you are connected to the drone's Wi-Fi network. 

> **Tip**: If you encounter issues connecting to the drone's Wi-Fi, try rebooting the drone by removing its battery and reinserting it. This often resolves connectivity problems.

1. Connection.
    - Connect to the drone by pressing the **Connect to Drone** button in the Connection Window. Make sure no warnings appear before starting the flight.
    - You can also turn on the camera feed after starting your drone by pressing the **Connect to Camera** button. However, that severely limits the range of connection.

2. Arm your drone's propellers. 
    - Press the **Arm propellers** button in the Conrol Window. The drone must be on a level surface to arm its propellers and take off.
    - In manual mode, arming the propellers also sets an idle throttle of 150. That means, instead of taking off you can press shift a couple of times to increase your throttle and lift off.

3. Take off. 
    - **The drone must be in manual mode for the takeoff.** Press the **Take off** button in the Control Window.
    - The manual mode controls the drone as if you are using the joystick, however it is controlled using your keyboard: 
        - **W and S** make the drone go forward and backwards.
        - **A and D** change the yaw.
        - **Q and E** make the drone go sideways left and right.
        - **Shift** increases the throttle by 50 out of a maximum 1000. You need to press shift several times to get more throttle, holding does nothing.
        - **Control** decreases the throttle by 50. You need to press control several times to get more throttle, holding does nothing.(The drone should hover at around 450 without any external modifications at medium battery voltage)
    - The stabilization mode is used for fine adjustment of the drone's velocity in it's local system of coordinates (relative to the drone's orientation) The controls are similar to manual mode:
        - **W and S** make the drone go forward and backwards. The drone slowly accelerates to 2 m/s.
        - **A and D** change the yaw.
        - **Q and E** make the drone go sideways left and right. The drone slowly accelerates to 2 m/s.
        - **Shift** makes the drone go up by 0.5m/s more. You need to press it several times to increase vertical speed even more.
        - **Control** makes the drone go down by 0.5m/s more. You need to press it several times to increase vertical speed even more.

4. Taking videos/photos mid-flight.
    - Before recording any video, make sure that the MicroSD Card is properly plugged into the drone.
    - Press the **Take picture** button to take a 600x800 photo onto your sd card.
    - Press the **Start video recording** button to start recording the video. If the command goes through successfully, the button will become **Stop video recording**, and once you press that the video will save.
    - Naming scheme: The files on the SD card are the time of recording and 2 random letters. For example: 172326OF.JPG. This means that the picture was taken at 17:23:26.

5. LED Control
    - If you are flying in dark conditions, turning on LEDs is advised. In the LED Control window you will find 4 color pickers responsible for changing the color of the 4 LEDs on the drone. Change the color of LEDs by setting the color and clicking the **apply button** at the bottom of LED Control window. Setting the color to black turns off the LED.

6. UI Control
    - Currently, you can only change the width of the sidebar by dragging the slider and clicking apply. Default is 300.

7. Script control
    - The drone can fly autonomously using lua. This section is under development.

8. Navbar
    - At the top of the screen there is a navbar showing the most important information about the state of the flight.
    - Battery: The battery voltage is shown. 4.2V is a fully charged battery. The critical battery voltage is 3.55V. Landing is advised at 3.7V.
    - Drone: shows the status of the connection, whether the drone is connected or not.
    - Camera: shows the status of the connection, whether the camera is connected and running or not.
    - Autopilot state: Shows the current mavlink autopilot state. It can be („ROOT“, „DISARMED“, „IDLE“, „TEST_ACTUATION“, „TEST_PARACHUTE“, „TEST_ENGINE“, „PARACHUTE“, „WAIT_FOR_LANDING“, „LANDED“, „CATAPULT“, „PREFLIGHT“, „ARMED“, „TAKEOFF“, „WAIT_FOR_GPS“, „WIND_MEASURE“, „MISSION“, „ASCEND“, „DESCEND“, „RTL“, „UNCONDITIONAL_RTL“, „MANUAL_HEADING“, „MANUAL_ROLL“, „MANUAL_SPEED“, „LANDING“, „ON_DEMAND“).
    - Altitude: Shows the altitude as seen by the rangefinder. It is not very accurate.
    - LPS: Shows the X Y Z position of the drone using dead reckoning. Can be inaccurate on long flights.

## Code structure
The code is divided into 2 packages (core and ui) and the main.py file.
### Core
This package contains the basic functionality to control the drone:
- app_state.py contains the current state of flight. It features a singleton class AppState.
- camera_controller.py contains the logic for displaying the live video feed, as well as recording video and taking pictures
- drone_controller.py contains everything needed to control the drone. connect_to_drone connects the application to the drone, set_led updates the drone's LEDs, toggle_arm arms and disarms the drone's propellers, takeoff and land make the drone take off and land (currently buggy, will fix later), control_mainloop is a function that controls the drone's flight in a separate thread.
- helper.py contains some functions for helping the app run. It features asynchronous wrappers, the filename generation function for recording video and taking pictures, and set_control_mode function for toggling between manual and stabilized control.
- pioneer_extensions contains a monkey patch to pioneer_sdk's Pioneer class for manual control.

### UI
This package deals with the app's interface.
- input_handlers.py contains the handle_key_input function, which maps the key presses to the appropriate drone controls.
- layout.py contains the draw_layout which draws everything on screen.
- misc.py contains the preload_camera_feed function, which fills the camera view with dummy data on startup (the fancy pattern you see), and the update_menubar function, which updates the menu bar periodically in a separate thread.
- resize.py contains the logic to resize the navbar, as well as the screen.

### main.py
This is the main file of the application. 
- It first starts a thread in which all asynchronous actions are performed
- After that it draws the main window and registers keypress handlers
- Then it starts the background threads for controlling the drone and updating the menu bar.
- Finally, it configures the main window a bit and starts dearpygui.

### misc
This folder contains other files used for testing purposes. It contains the images used in this readme, the dearpygui's demo, and a file to find out what numbers are mapped to what keys.

## Contributing Guidelines

We welcome contributions to the Pioneer Mini Controller project! To ensure a smooth collaboration, please follow these guidelines:

### Reporting Issues
- Before reporting an issue, check the [issue tracker](https://github.com/BUSH222/pioneer-mini-controller/issues) to see if it has already been reported.
- Provide a clear and descriptive title for the issue.
- Include steps to reproduce the issue, expected behavior, and actual behavior.
- Attach relevant logs, screenshots, or error messages if applicable.

### Submitting Pull Requests
1. **Fork the Repository**: Create a personal fork of the repository.
2. **Create a Branch**: Use a descriptive branch name (e.g., `feature/add-led-control` or `bugfix/fix-camera-connection`).
3. **Make Changes**: Ensure your code adheres to the project's coding standards and is well-documented.
4. **Test Your Changes**: Verify that your changes work as expected and do not break existing functionality.
5. **Submit a Pull Request**:
    - Provide a clear description of the changes made.
    - Reference any related issues (e.g., `Closes #123`).
    - Ensure your branch is up-to-date with the `main` branch before submitting.

### Coding Standards
- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code style. This is automatically enforced with github actions. Flake8 config is in the [tox.ini](/tox.ini) file.
- Use meaningful variable and function names.
- Write clear and concise comments where necessary.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
