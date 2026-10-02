# RoboSort

RoboSort is a personal robotics software project I built to simulate an autonomous robot that can detect, collect, navigate with, and sort objects in a changing environment.

I wanted to build something that combines several robotics and programming concepts into one working system instead of having separate small exercises. The project started as a simple robot movement simulation and gradually developed into a larger system with sensors, pathfinding, dynamic obstacles, a state machine, automated tests, and a live web dashboard.

---

## What does it do

The robot operates inside a simulated 20 × 20 grid environment.

The environment contains:

- static obstacles
- dynamic obstacles
- Type A and Type B objects
- an A sorting zone
- a B sorting zone

The robot has to find the objects, navigate through the environment, pick them up, and deliver them to the correct sorting zone.

The general process is:

```text
Sense
  ↓
Detect
  ↓
Plan
  ↓
Navigate
  ↓
Pick up
  ↓
Carry
  ↓
Sort
  ↓
Repeat
Main Features
Autonomous Navigation

The robot moves through a grid-based environment while avoiding blocked positions.

It uses the A* pathfinding algorithm with a Manhattan-distance heuristic to calculate routes to its targets.

The navigation system also keeps track of the current path so that the robot does not need to recalculate a complete path after every individual movement.

Simulated Sensors

The robot has three distance sensors:

Front
Left
Right

The sensor readings include simulated noise.

The front sensor takes multiple readings and averages them to reduce the effect of individual noisy measurements.

Dynamic Obstacles

The environment can change while the simulation is running.

A dynamic obstacle is introduced during the simulation so that the robot has to deal with a changing environment rather than only fixed obstacles.

Object Handling

The robot can:

detect objects
select the nearest object
pick up an object
carry an object
navigate to the correct sorting zone
drop the object

Objects are classified as Type A or Type B.

State Machine

The robot uses different states to represent what it is currently doing.

The current states are:

IDLE
SEARCHING
NAVIGATING_TO_OBJECT
PICKING_UP
CARRYING
NAVIGATING_TO_ZONE
SORTING
ERROR

This makes the robot's behavior easier to organize and monitor.

Statistics

The simulation records:

objects sorted
failed objects
sorting success rate
total robot moves
failed moves
planned path steps

These values are also displayed in the web dashboard.

Web Dashboard

The project includes a Flask web dashboard that allows the simulation to be monitored and controlled from a browser.

The dashboard displays:

robot position
robot direction
current state
carrying status
front, left, and right sensor readings
sorting statistics
simulation statistics
the 20 × 20 environment map
static and dynamic obstacles
objects and sorting zones
a live activity log

The available controls are:

Step
Run
Stop
Reset
Development Progress

RoboSort was developed incrementally rather than being written as one large program.

The main development stages were:

Basic robot movement
Turning and direction handling
Simulated sensors
Sensor noise and filtering
Object detection and sorting
Environment and obstacles
Multiple simulated sensors
Robot state management
A* pathfinding
Path caching and replanning
Object pickup and delivery
Dynamic obstacles
Automated tests
Simulation refactoring
Flask API
Live web dashboard
Live activity monitoring

This progression allowed the project to grow from a simple simulation into a more complete robotics software system.

How the System Works

The project is divided into several components instead of putting the whole simulation into one file.

                     Web Dashboard
                 HTML / CSS / JavaScript
                           |
                           v
                         Flask
                           |
                           v
                        JSON API
                           |
                           v
                     simulation.py
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      robot.py         sensor.py      environment.py
          |                                 |
          v                                 v
 state_machine.py                     obstacles / objects
          |
          v
   statistics.py

The Python side contains the actual robot and simulation logic.

Flask provides the interface between the simulation and the browser.

The JavaScript frontend requests the current state from Flask and updates the dashboard.

The state is exchanged as JSON.

API and JSON

The web dashboard communicates with the Python simulation through Flask API endpoints.

For example:

Browser
   |
   | GET /api/state
   v
Flask
   |
   v
simulation.get_state()
   |
   v
JSON
   |
   v
Browser

The current API endpoints are:

GET  /api/state
POST /api/step
POST /api/start
POST /api/stop
POST /api/reset

A simplified state response looks like:

{
    "step": 10,
    "position": [5, 2],
    "direction": "E",
    "state": "NAVIGATING_TO_OBJECT"
}

The JavaScript frontend reads this information and updates the dashboard.

Project Structure
RoboSort/
│
├── app.py
├── main.py
├── simulation.py
├── robot.py
├── environment.py
├── sensor.py
├── sorter.py
├── state_machine.py
├── statistics.py
├── visualization.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── app.js
│
├── tests/
│   ├── test_api.py
│   ├── test_environment.py
│   ├── test_navigation.py
│   └── test_robot.py
│
├── .gitignore
└── README.md

Important Files
environment.py

Defines the simulated world, including:

grid dimensions
static obstacles
dynamic obstacles
object positions
sorting zones
robot position
robot direction
movement validation
distance calculations
sensor.py

Contains the simulated distance sensors, including sensor noise and the front-sensor filtering logic.

robot.py

Contains the main robot behavior, including:

movement
obstacle checking
object detection
A* pathfinding
navigation
pickup and drop behavior
robot state
statistics interaction
state_machine.py

Defines and manages the different robot states.

statistics.py

Tracks robot and sorting performance during the simulation.

simulation.py

Connects the environment, sensors, robot behavior, state machine, and statistics into one simulation.

It also prepares the simulation state that is sent to the web dashboard and maintains the live activity log.

app.py

Creates the Flask web application and exposes the simulation through API endpoints.

app.js

Connects the browser interface to the Flask API.

It sends control requests, receives JSON data, updates the dashboard, updates the map, and displays recent simulation activity.

index.html

Defines the structure of the web dashboard.

style.css

Controls the layout and appearance of the dashboard.

visualization.py

Provides the terminal-based visualization of the simulation environment.

Technologies
Python
Flask
HTML
CSS
JavaScript
A* pathfinding
JSON
unittest
Git
GitHub
Running the Project
Requirements

Python 3 and Flask are required.

Install Flask with:

pip install flask
Run the Web Dashboard

From the RoboSort directory:

python app.py

Then open:

http://127.0.0.1:5000
Run the Terminal Simulation

The simulation can also be run directly with:

python main.py
Run the Tests

Run the complete test suite with:

python -m unittest discover

The current test suite contains 20 tests.

Testing

The project includes automated tests for both the simulation logic and the Flask API.

The tests cover areas including:

environment behavior
robot movement
navigation
pathfinding
API responses
simulation control
reset behavior

The current test suite passes all 20 tests.

Example Simulation Output

A simulation run produces statistics such as:

Objects sorted: ...
Objects failed: ...
Sorting success rate: ...%
Robot moves: ...
Failed moves: ...
Planned path steps: ...

The exact values can vary between runs because the simulation includes sensor noise and changing conditions.

Why I Built It

I wanted to build a project where several robotics and programming concepts work together in one system.

Instead of only implementing pathfinding or sensor simulation separately, I wanted the robot to have a complete workflow:

Sense
  ↓
Detect
  ↓
Plan
  ↓
Navigate
  ↓
Interact
  ↓
Sort

I also wanted to build a visual interface for the simulation so that I could monitor the robot and control it without relying only on terminal output.

What I Learned

Building RoboSort gave me practical experience with:

modular Python programming
classes and state management
simulation design
sensor simulation
sensor filtering
A* pathfinding
state machines
dynamic obstacles
automated testing
Flask
API design
JSON data exchange
JavaScript
HTML and CSS
Git and GitHub

One of the main things I learned from this project was how separate components can be connected into one larger system.

Limitations

RoboSort is currently a software simulation.

The robot, sensors, objects, obstacles, and movement are simulated rather than controlled using physical hardware.

The Flask dashboard is currently designed to run locally.

The project does not currently use real motors, physical distance sensors, or an actual robotic platform.

Future Improvements

Possible future improvements include:

configurable environments
additional object types
more dynamic obstacles
improved obstacle avoidance
performance graphs
simulation history
more advanced robot behaviors
Arduino or microcontroller integration
physical sensors and motors
deploying the dashboard online
Project Status

RoboSort is an ongoing personal project.

The current version includes:

the core robot simulation
simulated sensors
sensor filtering
A* navigation
dynamic obstacles
object pickup and sorting
a state machine
simulation statistics
a state machine
simulation statistics
automated testing
a Flask API
a live web dashboard
a live activity log

The project is structured so that additional robotics and hardware features can be added later.

Author:
Personal robotics and software project built as part of my learning in Robotics and Intelligent Systems.