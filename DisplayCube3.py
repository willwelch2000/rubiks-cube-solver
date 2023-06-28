from vpython import *
from time import *
from Cube3Util import *
from Cube3 import *
import math

class DisplayCube3:
    # Parameters
    _thin = 0.1
    _steps = 10
    _renderTime = 0.02
    _pauseTime = 0.5
    
    # Calculated from parameters
    _smallestAngle = math.pi/2/_steps
    
    # State variables
    _cube = None
    _boxes = [[[None for _ in range(3)] for _ in range(3)] for _ in range(6)]
    
    def __init__(self, cube):
        self._cube = cube
        self.setDisplay()
        
        addOnFunctions = {
            Action.TCW : self.turnClockwise,
            Action.TCCW : self.turnCounterClockwise,
            Action.TF : self.turnForward,
            Action.TB : self.turnBackward,
            Action.U : self.moveU,
            Action.D : self.moveD,
            Action.R : self.moveR,
            Action.L : self.moveL,
            Action.F : self.moveF,
            Action.B : self.moveB,
            Action.UP : self.moveUP,
            Action.DP : self.moveDP,
            Action.RP : self.moveRP,
            Action.LP : self.moveLP,
            Action.FP : self.moveFP,
            Action.BP : self.moveBP
        }
        cube.setAddOns(addOnFunctions)
        
    def setDisplay(self):
        rubiksColorToVector = {
            RubiksColor.BLUE : color.blue,
            RubiksColor.RED : color.red,
            RubiksColor.WHITE : color.white,
            RubiksColor.YELLOW : color.yellow,
            RubiksColor.ORANGE : color.orange,
            RubiksColor.GREEN : color.green
        }
        
        state = self._cube.getState()
        
        for face in Faces:
            for row in range(3):
                for col in range(3):
                    square = state[face.value][row][col]
                    (length, height, width, x, y, z) = DisplayCube3.getDisplaySpecs(face, row, col)
                    if (self._boxes[face.value][row][col] == None):
                        self._boxes[face.value][row][col] = box(color = rubiksColorToVector[square], length = length, height = height, width = width, pos = vector(x, y, z))
                    else:
                        self._boxes[face.value][row][col].color = rubiksColorToVector[square]
                        self._boxes[face.value][row][col].length = length
                        self._boxes[face.value][row][col].height = height
                        self._boxes[face.value][row][col].width = width
                        self._boxes[face.value][row][col].pos = (x, y, z)
                
                
    # Helper function for setDisplay
    
    def getDisplaySpecs(face, row, col):
        # Given cube coordinates, returns tuple consisting of: (length, height, width, x, y, z)
        
        if face == Faces.TOP:
            return (1, 1, DisplayCube3._thin, col - 1, -(row - 1), 1.5)
        if face == Faces.FRONT:
            return (1, DisplayCube3._thin, 1, col - 1, -1.5, -(row - 1))
        if face == Faces.RIGHT:
            return (DisplayCube3._thin, 1, 1, 1.5, col - 1, -(row - 1))
        if face == Faces.BACK:
            return (1, DisplayCube3._thin, 1, -(col - 1), 1.5, -(row - 1))
        if face == Faces.LEFT:
            return (DisplayCube3._thin, 1, 1, -1.5, -(col - 1), -(row - 1))
        if face == Faces.BOTTOM:
            return (1, 1, DisplayCube3._thin, col - 1, (row - 1), -1.5)
        
        
    # General functions for animation, adjusting boxes array
    def animate(self, axis, points):
        # Animate each point in points[] rotating 90 degrees around axis
        
        rotation = self._smallestAngle
        while rotation <= math.pi/2:
            sleep(self._renderTime)
            for (face, row, col) in points:
                # Revolve and rotate
                self._boxes[face.value][row][col].pos = rotate(self._boxes[face.value][row][col].pos, angle = self._smallestAngle, axis = axis)
                self._boxes[face.value][row][col].rotate(angle = self._smallestAngle, axis = axis)
            rotation += self._smallestAngle
        sleep(self._pauseTime)
        
    def adjustBoxes(self, action):
        # Adjust the _boxes array based on the transformations for the given action
        transformations = Cube3.getTransformations(action)
        newBoxes = stateCopy(self._boxes)
        
        for origin, destination, points, mapping in transformations:
            if mapping == None:
                mapping = getOrientationMapping(origin, destination)
            for point in points:
                coordsOfMappedPoint = mapping[point]
                newBoxes[destination.value][point[0]][point[1]] = self._boxes[origin.value][coordsOfMappedPoint[0]][coordsOfMappedPoint[1]]
        
        self._boxes = newBoxes
        
        
    # Turn functions
        
    def turnClockwise(self):
        # Do an animation of a full cube clockwise rotation
        
        points = [(face, r, c) for (r, c) in getAllPoints() for face in Faces]
        self.animate(vector(0, 0, -1), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.TCW)
        
    def turnCounterClockwise(self):
        # Do an animation of a full cube counterclockwise rotation
        
        points = [(face, r, c) for (r, c) in getAllPoints() for face in Faces]
        self.animate(vector(0, 0, 1), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.TCCW)
        
    def turnForward(self):
        # Do an animation of a full cube forward rotation
        
        points = [(face, r, c) for (r, c) in getAllPoints() for face in Faces]
        self.animate(vector(-1, 0, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.TF)
        
    def turnBackward(self):
        # Do an animation of a full cube forward rotation
        
        points = [(face, r, c) for (r, c) in getAllPoints() for face in Faces]
        self.animate(vector(1, 0, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.TB)
        
    
    # Move functions
    
    def moveU(self):
        # Do an animation of a U move
        
        points = [(Faces.TOP, r, c) for (r, c) in getAllPoints()]
        points.extend([(face, r, c) for (r, c) in getPointsInRow(0) for face in [Faces.FRONT, Faces.RIGHT, Faces.BACK, Faces.LEFT]])
        self.animate(vector(0, 0, -1), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.U)
    
    def moveUP(self):
        # Do an animation of a UP move
        
        points = [(Faces.TOP, r, c) for (r, c) in getAllPoints()]
        points.extend([(face, r, c) for (r, c) in getPointsInRow(0) for face in [Faces.FRONT, Faces.RIGHT, Faces.BACK, Faces.LEFT]])
        self.animate(vector(0, 0, 1), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.UP)
    
    def moveD(self):
        # Do an animation of a D move
        
        points = [(Faces.BOTTOM, r, c) for (r, c) in getAllPoints()]
        points.extend([(face, r, c) for (r, c) in getPointsInRow(2) for face in [Faces.FRONT, Faces.RIGHT, Faces.BACK, Faces.LEFT]])
        self.animate(vector(0, 0, 1), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.D)
    
    def moveDP(self):
        # Do an animation of a DP move
        
        points = [(Faces.BOTTOM, r, c) for (r, c) in getAllPoints()]
        points.extend([(face, r, c) for (r, c) in getPointsInRow(2) for face in [Faces.FRONT, Faces.RIGHT, Faces.BACK, Faces.LEFT]])
        self.animate(vector(0, 0, -1), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.DP)
        
    def moveR(self):
        # Do an animation of a R move
        
        points = [(Faces.RIGHT, r, c) for (r, c) in getAllPoints()]
        points.extend([(face, r, c) for (r, c) in getPointsInCol(2) for face in [Faces.FRONT, Faces.TOP, Faces.BOTTOM]])
        points.extend([(Faces.BACK, r, c) for (r, c) in getPointsInCol(0)])
        self.animate(vector(-1, 0, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.R)
        
    def moveRP(self):
        # Do an animation of a RP move
        
        points = [(Faces.RIGHT, r, c) for (r, c) in getAllPoints()]
        points.extend([(face, r, c) for (r, c) in getPointsInCol(2) for face in [Faces.FRONT, Faces.TOP, Faces.BOTTOM]])
        points.extend([(Faces.BACK, r, c) for (r, c) in getPointsInCol(0)])
        self.animate(vector(1, 0, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.RP)
        
    def moveL(self):
        # Do an animation of a L move
        
        points = [(Faces.LEFT, r, c) for (r, c) in getAllPoints()]
        points.extend([(face, r, c) for (r, c) in getPointsInCol(0) for face in [Faces.FRONT, Faces.TOP, Faces.BOTTOM]])
        points.extend([(Faces.BACK, r, c) for (r, c) in getPointsInCol(2)])
        self.animate(vector(1, 0, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.L)
        
    def moveLP(self):
        # Do an animation of a LP move
        
        points = [(Faces.LEFT, r, c) for (r, c) in getAllPoints()]
        points.extend([(face, r, c) for (r, c) in getPointsInCol(0) for face in [Faces.FRONT, Faces.TOP, Faces.BOTTOM]])
        points.extend([(Faces.BACK, r, c) for (r, c) in getPointsInCol(2)])
        self.animate(vector(-1, 0, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.LP)
        
    def moveF(self):
        # Do an animation of a F move
        
        points = [(Faces.FRONT, r, c) for (r, c) in getAllPoints()]
        points.extend([(Faces.TOP, r, c) for (r, c) in getPointsInRow(2)])
        points.extend([(Faces.RIGHT, r, c) for (r, c) in getPointsInCol(0)])
        points.extend([(Faces.BOTTOM, r, c) for (r, c) in getPointsInRow(0)])
        points.extend([(Faces.LEFT, r, c) for (r, c) in getPointsInCol(2)])
        self.animate(vector(0, 1, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.F)
        
    def moveFP(self):
        # Do an animation of a FP move
        
        points = [(Faces.FRONT, r, c) for (r, c) in getAllPoints()]
        points.extend([(Faces.TOP, r, c) for (r, c) in getPointsInRow(2)])
        points.extend([(Faces.RIGHT, r, c) for (r, c) in getPointsInCol(0)])
        points.extend([(Faces.BOTTOM, r, c) for (r, c) in getPointsInRow(0)])
        points.extend([(Faces.LEFT, r, c) for (r, c) in getPointsInCol(2)])
        self.animate(vector(0, -1, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.FP)
        
    def moveB(self):
        # Do an animation of a B move
        
        points = [(Faces.BACK, r, c) for (r, c) in getAllPoints()]
        points.extend([(Faces.TOP, r, c) for (r, c) in getPointsInRow(0)])
        points.extend([(Faces.RIGHT, r, c) for (r, c) in getPointsInCol(2)])
        points.extend([(Faces.BOTTOM, r, c) for (r, c) in getPointsInRow(2)])
        points.extend([(Faces.LEFT, r, c) for (r, c) in getPointsInCol(0)])
        self.animate(vector(0, -1, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.B)
        
    def moveBP(self):
        # Do an animation of a BP move
        
        points = [(Faces.BACK, r, c) for (r, c) in getAllPoints()]
        points.extend([(Faces.TOP, r, c) for (r, c) in getPointsInRow(0)])
        points.extend([(Faces.RIGHT, r, c) for (r, c) in getPointsInCol(2)])
        points.extend([(Faces.BOTTOM, r, c) for (r, c) in getPointsInRow(2)])
        points.extend([(Faces.LEFT, r, c) for (r, c) in getPointsInCol(0)])
        self.animate(vector(0, 1, 0), points)
        
        # Adjust _boxes array so that they represent the correct box
        self.adjustBoxes(Action.BP)
