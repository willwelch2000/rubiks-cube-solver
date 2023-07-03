# Rubik's Cube Solver

This project contains Python files that will generate an animation of a given Rubik's Cube being solved.

## Setup
1. Ensure that Python is installed
2. Use pip to install VPython
```bash
pip install vpython
```

## Usage
```bash
python CubeInterface.py
```
The program will ask for user input. It must be entered in the following format
* Enter each face in the order: top, front, right, back, left, bottom 
    * The top, bottom, right, and left are all oriented by moving one 90-degree rotation from the front
    * The back is oriented by rotating from the front to the right face and then to the back
* For each face, enter nine characters representing the colors of the squares on the face (r, g, b, w, y, o)
    * Go in the order: top row, middle row, bottom row
    * White space is allowed anywhere to make more readable 

After hitting enter, the program will open a browser window and generate a live animation of the Rubik's Cube being solved

## Files
RubiksCube.py 
* Contains class defining RubiksCube object.
* Allows outside code to define state of a Rubik's Cube.
* Contains functions for moves on a Rubik's Cube. The class manages the change in cube state for these moves.
* The class also has a solve function, which executes the moves needed to solve the cube. 

RubiksCubeUtil.py
* Contains helper functions and definitions for a Rubik's Cube.
* Used by RubiksCube.py, DisplayRubiksCube.py, RubiksCubeInterface.py, and RubiksCubeTest.py. 

DisplayRubiksCube.py
* Class that manages the 3-d display of a given RubiksCube object. 
* Attaches animation functions onto the existing RubiksCube.py move functions.

RubiksCubeInterface.py
* Program that asks user for input to define Rubik's Cube state and then shows animation of the cube being solved.
* Uses RubiksCube.py and DisplayRubiksCube.py. 

RubiksCubeTest.py
* Test program--for developer use.