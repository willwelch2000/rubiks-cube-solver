# Definitions of important things
# Mapping: a dictionary relating a destination point to its origin
    # orientation[destination coordinates as tuple] = origin coordinates as tuple
# Transformation: tuple consisting of: (origin face, destination face, list of points (tuples) in destination to change, optional mapping--if not given, inferred)
    # the mapping can be inferred as long as the origin face and destination face are adjacent faces
    # if the origin and destination are equal (maybe for a face rotation), then the mapping must be included
# Point: tuple consisting of: (face, row, col)
    # If face is known, then it's just a tuple of: (row, col)

from Cube3Util import *
from time import *

class Cube3:
    
    '''
    State variable defines all the colors on the cube.
    Defined as Color[3][3][6]:
        6 faces, each face is a 3x3 matrix, where each entry is from the Color Enum
        Faces are ordered: top, front, right, back, left, bottom
        On a face, the first index is the row, the second index is the column
            i.e. face[1][2] is the far right square of the middle row
        The front is the reference point for all face orientations
            The top, bottom, right, and left are all oriented by moving one 90-degree rotation from the front
            The back is oriented by rotating from the front to the right face and then to the back
    '''
    _state = [[[]]]
    
    # a dictionary mapping an Action Enum to a function pointer
    _actions = {}
    
    # a list of moves to solve the cube
    _movesPerformed = []
    
    def __init__(self, state = None):
        if state == None:
            self._state = stateDefault()
        else:
            self._state = stateCopy(state)
        
    def setActions(self, actions : dict):
        self._actions = actions
    
    def setState(self, state):
        # state should be a Color[3][3][6]
        self._state = stateCopy(state)
                    
    def getState(self):
        return stateCopy(self._state)
    
    
    # General function for transforming cube state
    
    def transform(self, transformations):
        # Performs a given list of transformations
        
        newState = stateCopy(self._state)
        
        for origin, destination, points, mapping in transformations:
            if mapping == None:
                mapping = getOrientationMapping(origin, destination)
            for point in points:
                coordsOfMappedPoint = mapping[point]
                newState[destination.value][point[0]][point[1]] = self._state[origin.value][coordsOfMappedPoint[0]][coordsOfMappedPoint[1]]
                
        self._state = newState
    
    
    # Functions to handle moves
    
    def performAction(self, action):
        self.transform(Cube3.getTransformations(action))
        self._movesPerformed.append(action)
        
        if self._actions.get(action) != None:
            f = self._actions[action]
            f()
        
    # Static helper function--also used by DisplayCube3
    def getTransformations(action):
        # Given action from Actions Enum, returns list of transformations
        
        transformations = []
        
        match action:
            case Action.TCW:
                # Add rotations for top and bottom face (counterclockwise for bottom)
                transformations.append((Faces.TOP, Faces.TOP, getAllPoints(), getRotationMapping()))
                transformations.append((Faces.BOTTOM, Faces.BOTTOM, getAllPoints(), getRotationMapping(True)))
                
                # Add remaining transformations
                transformations.append((Faces.RIGHT, Faces.FRONT, getAllPoints(), None))
                transformations.append((Faces.BACK, Faces.RIGHT, getAllPoints(), None))
                transformations.append((Faces.LEFT, Faces.BACK, getAllPoints(), None))
                transformations.append((Faces.FRONT, Faces.LEFT, getAllPoints(), None))
                
                return transformations
            case Action.TCCW:
                # Add rotations for top and bottom face (counterclockwise for top)
                transformations.append((Faces.TOP, Faces.TOP, getAllPoints(), getRotationMapping(True)))
                transformations.append((Faces.BOTTOM, Faces.BOTTOM, getAllPoints(), getRotationMapping()))
                
                # Add remaining transformations
                transformations.append((Faces.LEFT, Faces.FRONT, getAllPoints(), None))
                transformations.append((Faces.FRONT, Faces.RIGHT, getAllPoints(), None))
                transformations.append((Faces.RIGHT, Faces.BACK, getAllPoints(), None))
                transformations.append((Faces.BACK, Faces.LEFT, getAllPoints(), None))
                
                return transformations
            case Action.TF:
                # Add rotations for right and left face (counterclockwise for left)
                transformations.append((Faces.RIGHT, Faces.RIGHT, getAllPoints(), getRotationMapping()))
                transformations.append((Faces.LEFT, Faces.LEFT, getAllPoints(), getRotationMapping(True)))
                
                # Add remaining transformations
                transformations.append((Faces.FRONT, Faces.TOP, getAllPoints(), None))
                transformations.append((Faces.TOP, Faces.BACK, getAllPoints(), None))
                transformations.append((Faces.BACK, Faces.BOTTOM, getAllPoints(), None))
                transformations.append((Faces.BOTTOM, Faces.FRONT, getAllPoints(), None))
                
                return transformations
            case Action.TB:
                # Add rotations for right and left face (counterclockwise for right)
                transformations.append((Faces.RIGHT, Faces.RIGHT, getAllPoints(), getRotationMapping(True)))
                transformations.append((Faces.LEFT, Faces.LEFT, getAllPoints(), getRotationMapping()))
                
                # Add remaining transformations
                transformations.append((Faces.BACK, Faces.TOP, getAllPoints(), None))
                transformations.append((Faces.BOTTOM, Faces.BACK, getAllPoints(), None))
                transformations.append((Faces.FRONT, Faces.BOTTOM, getAllPoints(), None))
                transformations.append((Faces.TOP, Faces.FRONT, getAllPoints(), None))
                
                return transformations
            case Action.U:
                # Add rotation for top
                transformations.append((Faces.TOP, Faces.TOP, getAllPoints(), getRotationMapping()))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.RIGHT, Faces.FRONT, getPointsInRow(0), None))
                transformations.append((Faces.BACK, Faces.RIGHT, getPointsInRow(0), None))
                transformations.append((Faces.LEFT, Faces.BACK, getPointsInRow(0), None))
                transformations.append((Faces.FRONT, Faces.LEFT, getPointsInRow(0), None))
                
                return transformations
            case Action.UP:
                # Add rotation for top
                transformations.append((Faces.TOP, Faces.TOP, getAllPoints(), getRotationMapping(True)))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.LEFT, Faces.FRONT, getPointsInRow(0), None))
                transformations.append((Faces.FRONT, Faces.RIGHT, getPointsInRow(0), None))
                transformations.append((Faces.RIGHT, Faces.BACK, getPointsInRow(0), None))
                transformations.append((Faces.BACK, Faces.LEFT, getPointsInRow(0), None))
                
                return transformations
            case Action.D:
                # Add rotation for bottom
                transformations.append((Faces.BOTTOM, Faces.BOTTOM, getAllPoints(), getRotationMapping()))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.LEFT, Faces.FRONT, getPointsInRow(2), None))
                transformations.append((Faces.FRONT, Faces.RIGHT, getPointsInRow(2), None))
                transformations.append((Faces.RIGHT, Faces.BACK, getPointsInRow(2), None))
                transformations.append((Faces.BACK, Faces.LEFT, getPointsInRow(2), None))
                
                return transformations
            case Action.DP:
                # Add rotation for bottom
                transformations.append((Faces.BOTTOM, Faces.BOTTOM, getAllPoints(), getRotationMapping(True)))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.RIGHT, Faces.FRONT, getPointsInRow(2), None))
                transformations.append((Faces.BACK, Faces.RIGHT, getPointsInRow(2), None))
                transformations.append((Faces.LEFT, Faces.BACK, getPointsInRow(2), None))
                transformations.append((Faces.FRONT, Faces.LEFT, getPointsInRow(2), None))
                
                return transformations
            case Action.R:
                # Add rotation for right
                transformations.append((Faces.RIGHT, Faces.RIGHT, getAllPoints(), getRotationMapping()))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.FRONT, Faces.TOP, getPointsInCol(2), None))
                transformations.append((Faces.TOP, Faces.BACK, getPointsInCol(0), None))
                transformations.append((Faces.BACK, Faces.BOTTOM, getPointsInCol(2), None))
                transformations.append((Faces.BOTTOM, Faces.FRONT, getPointsInCol(2), None))
                
                return transformations
            case Action.RP:
                # Add rotation for right
                transformations.append((Faces.RIGHT, Faces.RIGHT, getAllPoints(), getRotationMapping(True)))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.BACK, Faces.TOP, getPointsInCol(2), None))
                transformations.append((Faces.BOTTOM, Faces.BACK, getPointsInCol(0), None))
                transformations.append((Faces.FRONT, Faces.BOTTOM, getPointsInCol(2), None))
                transformations.append((Faces.TOP, Faces.FRONT, getPointsInCol(2), None))
                
                return transformations
            case Action.L:
                # Add rotation for left
                transformations.append((Faces.LEFT, Faces.LEFT, getAllPoints(), getRotationMapping()))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.BACK, Faces.TOP, getPointsInCol(0), None))
                transformations.append((Faces.BOTTOM, Faces.BACK, getPointsInCol(2), None))
                transformations.append((Faces.FRONT, Faces.BOTTOM, getPointsInCol(0), None))
                transformations.append((Faces.TOP, Faces.FRONT, getPointsInCol(0), None))
                
                return transformations
            case Action.LP:
                # Add rotation for left
                transformations.append((Faces.LEFT, Faces.LEFT, getAllPoints(), getRotationMapping(True)))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.FRONT, Faces.TOP, getPointsInCol(0), None))
                transformations.append((Faces.TOP, Faces.BACK, getPointsInCol(2), None))
                transformations.append((Faces.BACK, Faces.BOTTOM, getPointsInCol(0), None))
                transformations.append((Faces.BOTTOM, Faces.FRONT, getPointsInCol(0), None))
                
                return transformations
            case Action.F:
                # Add rotation for front
                transformations.append((Faces.FRONT, Faces.FRONT, getAllPoints(), getRotationMapping()))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.LEFT, Faces.TOP, getPointsInRow(2), None))
                transformations.append((Faces.TOP, Faces.RIGHT, getPointsInCol(0), None))
                transformations.append((Faces.RIGHT, Faces.BOTTOM, getPointsInRow(0), None))
                transformations.append((Faces.BOTTOM, Faces.LEFT, getPointsInCol(2), None))
                
                return transformations
            case Action.FP:
                # Add rotation for front
                transformations.append((Faces.FRONT, Faces.FRONT, getAllPoints(), getRotationMapping(True)))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.RIGHT, Faces.TOP, getPointsInRow(2), None))
                transformations.append((Faces.BOTTOM, Faces.RIGHT, getPointsInCol(0), None))
                transformations.append((Faces.LEFT, Faces.BOTTOM, getPointsInRow(0), None))
                transformations.append((Faces.TOP, Faces.LEFT, getPointsInCol(2), None))
                
                return transformations
            case Action.B:
                # Add rotation for back
                transformations.append((Faces.BACK, Faces.BACK, getAllPoints(), getRotationMapping()))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.RIGHT, Faces.TOP, getPointsInRow(0), None))
                transformations.append((Faces.BOTTOM, Faces.RIGHT, getPointsInCol(2), None))
                transformations.append((Faces.LEFT, Faces.BOTTOM, getPointsInRow(2), None))
                transformations.append((Faces.TOP, Faces.LEFT, getPointsInCol(0), None))
                
                return transformations
            case Action.BP:
                # Add rotation for back
                transformations.append((Faces.BACK, Faces.BACK, getAllPoints(), getRotationMapping(True)))
                
                # Add transformations to switch the remaining individual squares
                transformations.append((Faces.LEFT, Faces.TOP, getPointsInRow(0), None))
                transformations.append((Faces.TOP, Faces.RIGHT, getPointsInCol(2), None))
                transformations.append((Faces.RIGHT, Faces.BOTTOM, getPointsInRow(2), None))
                transformations.append((Faces.BOTTOM, Faces.LEFT, getPointsInCol(0), None))
                
                return transformations
        

    # Solver function
    
    def solve(self):
        self._movesPerformed = []
        desiredState = stateDefault() # Building up state as we go on--starts at all default (no requirements)
        
        # 1: Orient cube
        self.orientCube(desiredState)
            
        # 2: White cross
        # white/blue edge
        desiredState[Faces.TOP.value][2][1] = RubiksColor.WHITE
        desiredState[Faces.FRONT.value][0][1] = RubiksColor.BLUE
        self.incrementLookahead(1, 4, desiredState)
        # white/orange edge
        desiredState[Faces.TOP.value][1][2] = RubiksColor.WHITE
        desiredState[Faces.RIGHT.value][0][1] = RubiksColor.ORANGE
        self.incrementLookahead(1, 4, desiredState)
        # white/green edge
        desiredState[Faces.TOP.value][0][1] = RubiksColor.WHITE
        desiredState[Faces.BACK.value][0][1] = RubiksColor.GREEN
        self.incrementLookahead(1, 4, desiredState)
        # white/red edge
        desiredState[Faces.TOP.value][1][0] = RubiksColor.WHITE
        desiredState[Faces.LEFT.value][0][1] = RubiksColor.RED
        self.incrementLookahead(1, 4, desiredState)
        
        # 3: White face
        self.doWhiteCorner(desiredState, RubiksColor.BLUE, RubiksColor.RED)
        self.doWhiteCorner(desiredState, RubiksColor.ORANGE, RubiksColor.BLUE)
        self.doWhiteCorner(desiredState, RubiksColor.RED, RubiksColor.GREEN)
        self.doWhiteCorner(desiredState, RubiksColor.GREEN, RubiksColor.ORANGE)
        
        # 4: Middle row edges
        self.doMiddleEdge(desiredState, RubiksColor.RED, RubiksColor.BLUE)
        self.doMiddleEdge(desiredState, RubiksColor.BLUE, RubiksColor.ORANGE)
        self.doMiddleEdge(desiredState, RubiksColor.ORANGE, RubiksColor.GREEN)
        self.doMiddleEdge(desiredState, RubiksColor.GREEN, RubiksColor.RED)
        
        # Cube is flipped upside down--desiredState not accurate
        
        # 5: Yellow cross
        tempDesiredState = stateDefault()
        tempDesiredState[Faces.TOP.value][0][1] = RubiksColor.YELLOW
        tempDesiredState[Faces.TOP.value][1][0] = RubiksColor.YELLOW
        tempDesiredState[Faces.TOP.value][1][2] = RubiksColor.YELLOW
        tempDesiredState[Faces.TOP.value][2][1] = RubiksColor.YELLOW
        desiredState[Faces.BOTTOM.value][0][1] = RubiksColor.YELLOW
        desiredState[Faces.BOTTOM.value][1][0] = RubiksColor.YELLOW
        desiredState[Faces.BOTTOM.value][1][2] = RubiksColor.YELLOW
        desiredState[Faces.BOTTOM.value][2][1] = RubiksColor.YELLOW
        topFace = self._state[Faces.TOP.value]
        if self.isDesiredState(tempDesiredState):
            pass
        elif RubiksColor.YELLOW not in [topFace[0][1], topFace[1][0], topFace[1][2], topFace[2][1]]:
            # No yellow edges
            self.performAction(Action.F)
            self.performAction(Action.U)
            self.performAction(Action.R)
            self.performAction(Action.UP)
            self.performAction(Action.RP)
            self.performAction(Action.FP)
        elif (topFace[0][1] == RubiksColor.YELLOW and topFace[2][1] == RubiksColor.YELLOW) or (topFace[1][0] == RubiksColor.YELLOW and topFace[1][2] == RubiksColor.YELLOW):
            # Straight line of yellow edges across
            if topFace[0][1] == RubiksColor.YELLOW and topFace[2][1] == RubiksColor.YELLOW:
                self.performAction(Action.U)
            self.performAction(Action.F)
            self.performAction(Action.R)
            self.performAction(Action.U)
            self.performAction(Action.RP)
            self.performAction(Action.UP)
            self.performAction(Action.FP)
        else:
            # Yellow L
            while not (topFace[0][1] == RubiksColor.YELLOW and topFace[1][0] == RubiksColor.YELLOW):
                self.performAction(Action.U)
                topFace = self._state[Faces.TOP.value]
            self.performAction(Action.F)
            self.performAction(Action.U)
            self.performAction(Action.R)
            self.performAction(Action.UP)
            self.performAction(Action.RP)
            self.performAction(Action.FP)
            
        # Cube is still upside down
            
        # 6 Yellow corners on top
        tempDesiredState = stateDefault()
        tempDesiredState[Faces.TOP.value][0][0] = RubiksColor.YELLOW
        tempDesiredState[Faces.TOP.value][0][2] = RubiksColor.YELLOW
        tempDesiredState[Faces.TOP.value][2][0] = RubiksColor.YELLOW
        tempDesiredState[Faces.TOP.value][2][2] = RubiksColor.YELLOW
        desiredState[Faces.BOTTOM.value][0][0] = RubiksColor.YELLOW
        desiredState[Faces.BOTTOM.value][0][2] = RubiksColor.YELLOW
        desiredState[Faces.BOTTOM.value][2][0] = RubiksColor.YELLOW
        desiredState[Faces.BOTTOM.value][2][2] = RubiksColor.YELLOW
        
        # Loop until complete
        while not self.isDesiredState(tempDesiredState):
            # Find how many corners are yellow
            numberYellowCorners = sum([1 for coords in [(0, 0), (0, 2), (2, 0), (2, 2)] if self._state[Faces.TOP.value][coords[0]][coords[1]] == RubiksColor.YELLOW])
            if numberYellowCorners == 1:
                while self._state[Faces.TOP.value][2][0] != RubiksColor.YELLOW:
                    self.performAction(Action.U)
            else:
                while self._state[Faces.FRONT.value][0][0] != RubiksColor.YELLOW:
                    self.performAction(Action.U)
            self.performAction(Action.R)
            self.performAction(Action.U)
            self.performAction(Action.RP)
            self.performAction(Action.U)
            self.performAction(Action.R)
            self.performAction(Action.U)
            self.performAction(Action.U)
            self.performAction(Action.RP)
            
        # 7: Yellow corners in place
        self.orientCube(upsideDown = True)
        tempDesiredState = stateDefault()
        tempDesiredState[Faces.FRONT.value][0][0] = RubiksColor.BLUE
        tempDesiredState[Faces.FRONT.value][0][2] = RubiksColor.BLUE
        tempDesiredState[Faces.BACK.value][0][0] = RubiksColor.GREEN
        tempDesiredState[Faces.BACK.value][0][2] = RubiksColor.GREEN
        tempDesiredState[Faces.BOTTOM.value][0][0] = RubiksColor.WHITE
        tempDesiredState[Faces.BOTTOM.value][0][2] = RubiksColor.WHITE
        tempDesiredState[Faces.BOTTOM.value][2][0] = RubiksColor.WHITE
        tempDesiredState[Faces.BOTTOM.value][2][2] = RubiksColor.WHITE
        desiredState[Faces.FRONT.value][2][0] = RubiksColor.BLUE
        desiredState[Faces.FRONT.value][2][2] = RubiksColor.BLUE
        desiredState[Faces.RIGHT.value][2][0] = RubiksColor.ORANGE
        desiredState[Faces.RIGHT.value][2][2] = RubiksColor.ORANGE
        desiredState[Faces.BACK.value][2][0] = RubiksColor.GREEN
        desiredState[Faces.BACK.value][2][2] = RubiksColor.GREEN
        desiredState[Faces.LEFT.value][2][0] = RubiksColor.RED
        desiredState[Faces.LEFT.value][2][2] = RubiksColor.RED
        
        if not self.incrementLookahead(1, 2, tempDesiredState):
            twoYellowCornersCorrect = False
            for face in [Faces.FRONT, Faces.RIGHT, Faces.BACK, Faces.LEFT]:
                if self._state[face.value][0][0] == self._state[face.value][0][2]:
                    twoYellowCornersCorrect = True
                    break
            
            while True:
                if twoYellowCornersCorrect:
                    # Position solved on back
                    while not (self._state[Faces.BACK.value][0][0] == self._state[Faces.BACK.value][0][2]):
                        self.performAction(Action.U)
                
                # Do sequence
                self.performAction(Action.RP)
                self.performAction(Action.F)
                self.performAction(Action.RP)
                self.performAction(Action.B)
                self.performAction(Action.B)
                self.performAction(Action.R)
                self.performAction(Action.FP)
                self.performAction(Action.RP)
                self.performAction(Action.B)
                self.performAction(Action.B)
                self.performAction(Action.R)
                self.performAction(Action.R)
                
                if twoYellowCornersCorrect:
                    break
                else:
                    twoYellowCornersCorrect = True
            
            self.incrementLookahead(1, 2, tempDesiredState)
            
        # 8: Edges in place
        self.orientCube(upsideDown = True)
        tempDesiredState = stateDefault()
        tempDesiredState[Faces.FRONT.value][0][1] = RubiksColor.BLUE
        tempDesiredState[Faces.RIGHT.value][0][1] = RubiksColor.RED
        tempDesiredState[Faces.BACK.value][0][1] = RubiksColor.GREEN
        tempDesiredState[Faces.LEFT.value][0][1] = RubiksColor.ORANGE
        desiredState[Faces.FRONT.value][2][1] = RubiksColor.BLUE
        desiredState[Faces.RIGHT.value][2][1] = RubiksColor.ORANGE
        desiredState[Faces.BACK.value][2][1] = RubiksColor.GREEN
        desiredState[Faces.LEFT.value][2][1] = RubiksColor.RED
        
        if not self.isDesiredState(tempDesiredState):
            oneYellowEdgeSolved = False
            for face in [Faces.FRONT, Faces.RIGHT, Faces.BACK, Faces.LEFT]:
                if self._state[face.value][0][1] == self._state[face.value][0][2]:
                    oneYellowEdgeSolved = True
                    break
                
            while True:
                if oneYellowEdgeSolved:
                    # Rotate until solved on back
                    while self._state[Faces.BACK.value][0][1] != self._state[Faces.BACK.value][0][2]:
                        self.performAction(Action.TCW)
                        
                # Do sequence
                if not oneYellowEdgeSolved or self._state[Faces.RIGHT.value][0][1] == self._state[Faces.FRONT.value][0][0]:
                    self.performAction(Action.F)
                    self.performAction(Action.F)
                    self.performAction(Action.U)
                    self.performAction(Action.RP)
                    self.performAction(Action.L)
                    self.performAction(Action.F)
                    self.performAction(Action.F)
                    self.performAction(Action.R)
                    self.performAction(Action.LP)
                    self.performAction(Action.U)
                    self.performAction(Action.F)
                    self.performAction(Action.F)
                else:
                    self.performAction(Action.F)
                    self.performAction(Action.F)
                    self.performAction(Action.UP)
                    self.performAction(Action.RP)
                    self.performAction(Action.L)
                    self.performAction(Action.F)
                    self.performAction(Action.F)
                    self.performAction(Action.R)
                    self.performAction(Action.LP)
                    self.performAction(Action.UP)
                    self.performAction(Action.F)
                    self.performAction(Action.F)
                
                if oneYellowEdgeSolved:
                    break
                else:
                    oneYellowEdgeSolved = True
            
            print("Solved!")
            
    # Helper functions for solver
    
    def findFace(self, color):
        # Finds face (from Faces Enum) based on its center color
        for face in Faces:
            if (self._state[face.value][1][1] == color):
                return face
        return None
    
    def findEdge(self, color1, color2):
        # Finds an edge given the two colors
        # The point returned corresponds to the first color given
        pairs = [
            [(Faces.TOP, 0, 1), (Faces.BACK, 0, 1)],
            [(Faces.TOP, 1, 0), (Faces.LEFT, 0, 1)],
            [(Faces.TOP, 1, 2), (Faces.RIGHT, 0, 1)],
            [(Faces.TOP, 2, 1), (Faces.FRONT, 0, 1)],
            
            [(Faces.BOTTOM, 0, 1), (Faces.FRONT, 2, 1)],
            [(Faces.BOTTOM, 1, 0), (Faces.LEFT, 2, 1)],
            [(Faces.BOTTOM, 1, 2), (Faces.RIGHT, 2, 1)],
            [(Faces.BOTTOM, 2, 1), (Faces.BACK, 2, 1)],
            
            [(Faces.FRONT, 1, 0), (Faces.LEFT, 1, 2)],
            [(Faces.FRONT, 1, 2), (Faces.RIGHT, 1, 0)],
            [(Faces.BACK, 1, 0), (Faces.RIGHT, 1, 2)],
            [(Faces.BACK, 1, 2), (Faces.LEFT, 1, 0)]
        ]
        
        for (face1, r1, c1), (face2, r2, c2) in pairs:
            if self._state[face1.value][r1][c1] == color1 and self._state[face2.value][r2][c2] == color2:
                return (face1, r1, c1)
            if self._state[face1.value][r1][c1] == color2 and self._state[face2.value][r2][c2] == color1:
                return (face2, r2, c2)
        
        return None

    def findCorner(self, color1, color2, color3):
        # Finds a corner given the three colors
        # The point returned corresponds to the first color given
        groups = [
            [(Faces.TOP, 0, 0), (Faces.BACK, 0, 2), (Faces.LEFT, 0, 0)],
            [(Faces.TOP, 0, 2), (Faces.BACK, 0, 0), (Faces.RIGHT, 0, 2)],
            [(Faces.TOP, 2, 0), (Faces.FRONT, 0, 0), (Faces.LEFT, 0, 2)],
            [(Faces.TOP, 2, 2), (Faces.FRONT, 0, 2), (Faces.RIGHT, 0, 0)],
            
            [(Faces.BOTTOM, 2, 0), (Faces.BACK, 2, 2), (Faces.LEFT, 2, 0)],
            [(Faces.BOTTOM, 2, 2), (Faces.BACK, 2, 0), (Faces.RIGHT, 2, 2)],
            [(Faces.BOTTOM, 0, 0), (Faces.FRONT, 2, 0), (Faces.LEFT, 2, 2)],
            [(Faces.BOTTOM, 0, 2), (Faces.FRONT, 2, 2), (Faces.RIGHT, 2, 0)]
        ]
        
        for (face1, r1, c1), (face2, r2, c2), (face3, r3, c3) in groups:
            if self._state[face1.value][r1][c1] == color1:
                if (self._state[face2.value][r2][c2] == color2 and self._state[face3.value][r3][c3] == color3) or (self._state[face2.value][r2][c2] == color3 and self._state[face3.value][r3][c3] == color2):
                    return (face1, r1, c1)
            if self._state[face2.value][r2][c2] == color1:
                if (self._state[face1.value][r1][c1] == color2 and self._state[face3.value][r3][c3] == color3) or (self._state[face1.value][r1][c1] == color3 and self._state[face3.value][r3][c3] == color2):
                    return (face2, r2, c2)
            if self._state[face3.value][r3][c3] == color1:
                if (self._state[face1.value][r1][c1] == color2 and self._state[face2.value][r2][c2] == color3) or (self._state[face1.value][r1][c1] == color3 and self._state[face2.value][r2][c2] == color2):
                    return (face3, r3, c3)
        
        return None
    
    def isDesiredState(self, desiredState):
        # Compares ._state to desiredState
        # desiredState is formatted just like _state, but DEFAULT means don't-care
        for face in Faces:
            for row in range(3):
                for col in range(3):
                    if desiredState[face.value][row][col] != RubiksColor.DEFAULT and desiredState[face.value][row][col] != self._state[face.value][row][col]:
                        return False
        return True
    
    def lookahead(self, steps, desiredState, movesMade = [], includeTurns = False):
        # Looks given # of steps into the future, trying to achieve desiredState
        # desiredState is formatted just like _state, but DEFAULT means don't-care
        # Returns list of moves to take, or None
                        
        if self.isDesiredState(desiredState):
            return movesMade
        
        if steps == 0:
            return None
        
        # Recursively try actions
        for action in Action:
            if (not includeTurns) and action in [Action.TCW, Action.TCCW, Action.TF, Action.TB]:
                continue
            cubeCopy = Cube3(self._state)
            moves = []
            moves.extend(movesMade)
            moves.append(action)
            cubeCopy.performAction(action)
            lookahead = cubeCopy.lookahead(steps - 1, desiredState, moves, includeTurns = includeTurns)
            if lookahead != None:
                return lookahead
            
        return None
    
    def incrementLookahead(self, minSteps, maxSteps, desiredState, includeTurns = False):
        # Does lookahead at minSteps, then increases stepsize to maxSteps
        # Returns False if not possible in # of steps, True otherwise
        if self.isDesiredState(desiredState):
            return True
        for i in range(minSteps, maxSteps + 1):
            actions = self.lookahead(i, desiredState, includeTurns = includeTurns)
            if actions != None:
                break
        if actions == None:
            return False
        for action in actions:
            self.performAction(action)
        return True
    
    
    # Subfunctions for solver
    
    def orientCube(self, desiredState = None, upsideDown = False):
        # Orients cube with white on top and blue at front if !upsideDown
        # Orients cube with yellow on top and blue at front if upsideDown
        # Optional desiredState pointer argument--if passed, this initializes and edits that array by reference.
        # Otherwise, this just makes its own array
        
        if desiredState == None:
            desiredState = stateDefault() # Building up state as we go on--starts at all default (no requirements)
        
        desiredState[Faces.TOP.value][1][1] = RubiksColor.WHITE if not upsideDown else RubiksColor.YELLOW
        desiredState[Faces.FRONT.value][1][1] = RubiksColor.BLUE
        desiredState[Faces.RIGHT.value][1][1] = RubiksColor.ORANGE if not upsideDown else RubiksColor.RED
        desiredState[Faces.BACK.value][1][1] = RubiksColor.GREEN
        desiredState[Faces.LEFT.value][1][1] = RubiksColor.RED if not upsideDown else RubiksColor.ORANGE
        desiredState[Faces.BOTTOM.value][1][1] = RubiksColor.YELLOW if not upsideDown else RubiksColor.WHITE
        self.incrementLookahead(1, 4, desiredState, True)
    
    def doWhiteCorner(self, desiredState, color2, color3):
        # Get a white corner into place given 3 colors
        # Must be done in this order: wbr, wob, wrg, wgo--colors 2 and 3 cannot be interchanged
        
        # Adjust desired state to include corner
        if color2 == RubiksColor.BLUE and color3 == RubiksColor.RED:
            desiredState[Faces.TOP.value][2][0] = RubiksColor.WHITE
            desiredState[Faces.FRONT.value][0][0] = RubiksColor.BLUE
            desiredState[Faces.LEFT.value][0][2] = RubiksColor.RED
        elif color2 == RubiksColor.ORANGE and color3 == RubiksColor.BLUE:
            desiredState[Faces.TOP.value][2][2] = RubiksColor.WHITE
            desiredState[Faces.FRONT.value][0][2] = RubiksColor.BLUE
            desiredState[Faces.RIGHT.value][0][0] = RubiksColor.ORANGE
        elif color2 == RubiksColor.RED and color3 == RubiksColor.GREEN:
            desiredState[Faces.TOP.value][0][0] = RubiksColor.WHITE
            desiredState[Faces.BACK.value][0][2] = RubiksColor.GREEN
            desiredState[Faces.LEFT.value][0][0] = RubiksColor.RED
        elif color2 == RubiksColor.GREEN and color3 == RubiksColor.ORANGE:
            desiredState[Faces.TOP.value][0][2] = RubiksColor.WHITE
            desiredState[Faces.BACK.value][0][0] = RubiksColor.GREEN
            desiredState[Faces.RIGHT.value][0][2] = RubiksColor.ORANGE
            
        if self.incrementLookahead(1, 3, desiredState):
            return
        
        # Locate where corner is now
        corner = self.findCorner(RubiksColor.WHITE, color2, color3)
        
        # If white part of corner is on bottom face, perform sequence until it is on bottom row of a non top/bottom face
        if corner[0] == Faces.BOTTOM:
            if corner[1] == 0 and corner[2] == 2:
                self.performAction(Action.D)
            corner = self.findCorner(RubiksColor.WHITE, color2, color3)
            while corner[0] == Faces.BOTTOM or corner[1] == 0:
                self.performAction(Action.R)
                self.performAction(Action.D)
                self.performAction(Action.RP)
                self.performAction(Action.D)
                corner = self.findCorner(RubiksColor.WHITE, color2, color3)
                
        # If white part of corner is on TOP but not correct spot, get it on bottom row of non top/bottom face
        if corner[0] == Faces.TOP:
            if corner[1] == 0 and corner[2] == 0:
                self.performAction(Action.B)
                self.performAction(Action.D)
                self.performAction(Action.BP)
            if corner[1] == 0 and corner[2] == 2:
                self.performAction(Action.BP)
                self.performAction(Action.DP)
                self.performAction(Action.B)
            if corner[1] == 2 and corner[2] == 0:
                self.performAction(Action.FP)
                self.performAction(Action.DP)
                self.performAction(Action.F)
            if corner[1] == 2 and corner[2] == 2:
                self.performAction(Action.F)
                self.performAction(Action.D)
                self.performAction(Action.FP)
        
        # If white part of corner is on top row of non top/bottom face, get it on bottom row of non top/bottom face
        if corner[0] in [Faces.FRONT, Faces.RIGHT, Faces.BACK, Faces.LEFT] and corner[1] == 0:
            if corner == (Faces.FRONT, 0, 0):
                self.performAction(Action.FP)
                self.performAction(Action.DP)
                self.performAction(Action.F)
            elif corner == (Faces.FRONT, 0, 2):
                self.performAction(Action.F)
                self.performAction(Action.D)
                self.performAction(Action.FP)
            elif corner == (Faces.RIGHT, 0, 0):
                self.performAction(Action.RP)
                self.performAction(Action.DP)
                self.performAction(Action.R)
            elif corner == (Faces.RIGHT, 0, 2):
                self.performAction(Action.R)
                self.performAction(Action.D)
                self.performAction(Action.RP)
            elif corner == (Faces.BACK, 0, 0):
                self.performAction(Action.BP)
                self.performAction(Action.DP)
                self.performAction(Action.B)
            elif corner == (Faces.BACK, 0, 2):
                self.performAction(Action.B)
                self.performAction(Action.D)
                self.performAction(Action.BP)
            elif corner == (Faces.LEFT, 0, 0):
                self.performAction(Action.LP)
                self.performAction(Action.DP)
                self.performAction(Action.L)
            elif corner == (Faces.LEFT, 0, 2):
                self.performAction(Action.L)
                self.performAction(Action.D)
                self.performAction(Action.LP)
            
        # Now on bottom row--get to correct spot on bottom row
        while not self.whiteCornerBelowCorrectSpot(color2, color3):
            self.performAction(Action.D)
            
        # Now corner should be on non top/bottom face, bottom row
        self.incrementLookahead(3, 3, desiredState)
        
    def whiteCornerBelowCorrectSpot(self, color2, color3):
        # Checks if the given white corner is on the bottom row and directly below its correct spot
        corner = self.findCorner(RubiksColor.WHITE, color2, color3)
        if color2 == RubiksColor.BLUE and color3 == RubiksColor.RED:
            if corner in [(Faces.FRONT, 2, 0), (Faces.LEFT, 2, 2)]:
                return True
        if color2 == RubiksColor.ORANGE and color3 == RubiksColor.BLUE:
            if corner in [(Faces.FRONT, 2, 2), (Faces.RIGHT, 2, 0)]:
                return True
        if color2 == RubiksColor.RED and color3 == RubiksColor.GREEN:
            if corner in [(Faces.BACK, 2, 2), (Faces.LEFT, 2, 0)]:
                return True
        if color2 == RubiksColor.GREEN and color3 == RubiksColor.ORANGE:
            if corner in [(Faces.BACK, 2, 0), (Faces.RIGHT, 2, 2)]:
                return True
            
        return False
    
    def doMiddleEdge(self, desiredState, color1, color2):
        # Get a middle edge into place given 2 colors
        # Expected in this order: rb, bo, og, gr
        # Leaves the cube upside down after complete
    
        # Adjust desired state to include edge
        if color1 == RubiksColor.RED and color2 == RubiksColor.BLUE:
            desiredState[Faces.LEFT.value][1][2] = RubiksColor.RED
            desiredState[Faces.FRONT.value][1][0] = RubiksColor.BLUE
        elif color1 == RubiksColor.BLUE and color2 == RubiksColor.ORANGE:
            desiredState[Faces.FRONT.value][1][2] = RubiksColor.BLUE
            desiredState[Faces.RIGHT.value][1][0] = RubiksColor.ORANGE
        elif color1 == RubiksColor.ORANGE and color2 == RubiksColor.GREEN:
            desiredState[Faces.RIGHT.value][1][2] = RubiksColor.ORANGE
            desiredState[Faces.BACK.value][1][0] = RubiksColor.GREEN
        elif color1 == RubiksColor.GREEN and color2 == RubiksColor.RED:
            desiredState[Faces.BACK.value][1][2] = RubiksColor.GREEN
            desiredState[Faces.LEFT.value][1][0] = RubiksColor.RED
            
        if self.isDesiredState(desiredState):
            return
        
        # Flip upside down
        self.orientCube(upsideDown = True)
        
        edge = self.findEdge(color1, color2)
        
        # If edge is in middle row, move it out
        if edge[0] in [Faces.FRONT, Faces.RIGHT, Faces.BACK, Faces.LEFT] and edge[1] == 1:
            while edge not in [(Faces.FRONT, 1, 0), (Faces.LEFT, 1, 2)]:
                self.performAction(Action.TCW)
                edge = self.findEdge(color1, color2)
                
            # Do sequence
            self.performAction(Action.LP)
            self.performAction(Action.UP)
            self.performAction(Action.L)
            self.performAction(Action.U)
            self.performAction(Action.F)
            self.performAction(Action.U)
            self.performAction(Action.FP)
            
        edge = self.findEdge(color1, color2)
        nonTopColor = color2 if edge[0] == Faces.TOP else color1
                
        # Rotate until correct face is in front
        while self.findFace(nonTopColor) != Faces.FRONT:
            self.performAction(Action.TCW)
            
        edge = self.findEdge(color1, color2)
        if nonTopColor == color2:
            # Rotate top until it's opposite its color
            while edge != (Faces.TOP, 1, 0):
                self.performAction(Action.U)
                edge = self.findEdge(color1, color2)
            
            # Do sequence
            self.performAction(Action.R)
            self.performAction(Action.U)
            self.performAction(Action.RP)
            self.performAction(Action.UP)
            self.performAction(Action.FP)
            self.performAction(Action.UP)
            self.performAction(Action.F)
        else:
            # Rotate top until it's opposite its color
            while edge != (Faces.RIGHT, 0, 1):
                self.performAction(Action.U)
                edge = self.findEdge(color1, color2)
            
            # Do sequence
            self.performAction(Action.LP)
            self.performAction(Action.UP)
            self.performAction(Action.L)
            self.performAction(Action.U)
            self.performAction(Action.F)
            self.performAction(Action.U)
            self.performAction(Action.FP)
        
