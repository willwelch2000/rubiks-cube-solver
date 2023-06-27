from enum import Enum

class RubiksColor(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    WHITE = 3
    YELLOW = 4
    ORANGE = 5
    DEFAULT = 6
class Action(Enum):
    TCW = 0     # Turn whole cube clockwise
    TCCW = 1    # Turn whole cube counterclockwise
    TF = 2      # Turn whole cube forward
    TB = 3      # Turn whole cube backward
    U = 4       # Move upper face clockwise
    UP = 5      # Move upper face counterlockwise
    D = 6       # Move down face clockwise
    DP = 7      # Move down face counterlockwise
    R = 8       # Move right face clockwise
    RP = 9      # Move right face counterlockwise
    L = 10      # Move left face clockwise
    LP = 11     # Move left face counterlockwise
    F = 12      # Move front face clockwise
    FP = 13     # Move front face counterlockwise
    B = 14      # Move back face clockwise
    BP = 15     # Move back face counterlockwise
class Faces(Enum):
    TOP = 0
    FRONT = 1
    RIGHT = 2
    BACK = 3
    LEFT = 4
    BOTTOM = 5

# Actions besides whole-cube turns
moveActions = [
    Action.U,
    Action.D,
    Action.R,
    Action.L,
    Action.F,
    Action.B,
    Action.UP,
    Action.DP,
    Action.RP,
    Action.LP,
    Action.FP,
    Action.BP
]

def getOrientationMapping(origin, destination):
    # Function to define orientation differences between two faces' coordinate systems
    # Used during any move to know the coordinates on a new face for shifted squares
    # Input: origin face, destination face--should both be from Faces enum
    # Output: mapping between two faces
        
    # Define default
    orientation = {
        (row, col) : (row, col) for row in range(3) for col in range(3)
    }
    
    # Top as origin
    if (origin == Faces.TOP and destination == Faces.RIGHT):
        return {
            (r, c) : (2-c, r) for r in range(3) for c in range(3)
        }
        
    if (origin == Faces.TOP and destination == Faces.BACK):
        return {
            (r, c) : (2-r, 2-c) for r in range(3) for c in range(3)
        }
    
    if (origin == Faces.TOP and destination == Faces.LEFT):
        return {
            (r, c) : (c, 2-r) for r in range(3) for c in range(3)
        }
        
    # Front as origin--none to worry about
    
    # Right as origin
    if (origin == Faces.RIGHT and destination == Faces.TOP):
        return {
            (r, c) : (c, 2-r) for r in range(3) for c in range(3)
        }
    
    if (origin == Faces.RIGHT and destination == Faces.BOTTOM):
        return {
            (r, c) : (2-c, r) for r in range(3) for c in range(3)
        }
        
    # Back as origin
    if (origin == Faces.BACK and destination == Faces.TOP):
        return {
            (r, c) : (2-r, 2-c) for r in range(3) for c in range(3)
        }
    
    if (origin == Faces.BACK and destination == Faces.BOTTOM):
        return {
            (r, c) : (2-r, 2-c) for r in range(3) for c in range(3)
        }
        
    # Left as origin
    if (origin == Faces.LEFT and destination == Faces.TOP):
        return {
            (r, c) : (2-c, r) for r in range(3) for c in range(3)
        }
    
    if (origin == Faces.LEFT and destination == Faces.BOTTOM):
        return {
            (r, c) : (c, 2-r) for r in range(3) for c in range(3)
        }
        
    # Bottom as origin
    if (origin == Faces.BOTTOM and destination == Faces.RIGHT):
        return {
            (r, c) : (c, 2-r) for r in range(3) for c in range(3)
        }
    
    if (origin == Faces.BOTTOM and destination == Faces.BACK):
        return {
            (r, c) : (2-r, 2-c) for r in range(3) for c in range(3)
        }
    
    if (origin == Faces.BOTTOM and destination == Faces.LEFT):
        return {
            (r, c) : (2-c, r) for r in range(3) for c in range(3)
        }
     
    
    return orientation

def stateCopy(state):
    return [[[state[face][row][square] for square in range(3)] for row in range(3)] for face in range(6)]

def stateDefault():
    return [[[RubiksColor.DEFAULT for _ in range(3)] for _ in range(3)] for _ in range(6)]
    
def getRotationMapping(counterClockwise = False):
    # Returns a mapping of a simple rotation (clockwise by default)
    if (counterClockwise):
        return {
            (r, c) : (c, 2-r) for r in range(3) for c in range(3)
        }
    else:
        return {
            (r, c) : (2-c, r) for r in range(3) for c in range(3)
        }

def getOrientedFace(mapping, face):
    # Given an orientation mapping and a face, returns the correctly oriented face
    return [[face[mapping[(r, c)][0]][mapping[(r, c)][1]] for c in range(3)] for r in range(3)]

def getPointsInRow(row):
    return [(row, col) for col in range(3)]

def getPointsInCol(col):
    return [(row, col) for row in range(3)]

def getAllPoints():
    return [(row, col) for row in range(3) for col in range(3)]

def parseCube3State(stateStr):
    ''' Creates and returns a state object, given the state as a string
        The string must be formatted in this order:
            Face order: TOP, FRONT, RIGHT, BACK, LEFT, BOTTOM
            Within a face: top row, middle row, bottom row
            Each row goes left to right
        There should be one character per square
        Each character should be the first letter of the square it represents
            'w', 'b', 'g', 'y', 'o', or 'r'
    '''
    charToColor = {
        'w' : RubiksColor.WHITE,
        'b' : RubiksColor.BLUE,
        'g' : RubiksColor.GREEN,
        'y' : RubiksColor.YELLOW,
        'o' : RubiksColor.ORANGE,
        'r' : RubiksColor.RED
    }
    
    state = [[[RubiksColor.DEFAULT for _ in range(3)] for _ in range(3)] for _ in range(6)]
    
    for face in range(6):
        for row in range(3):
            for col in range(3):
                state[face][row][col] = charToColor[stateStr[face*9+row*3+col]]
                
    return state


# def getRotatedFace(face, counterClockwise = False):
#     # Returns a new rotated version of the face (clockwise by default)
#     if (counterClockwise):
#         return [[face[j][i] for j in range(3)] for i in range(2, -1, -1)]
#     else:
#         return [[face[j][i] for j in range(2, -1, -1)] for i in range(3)]

# def getFlippedFace(face):
#     # Returns a new flipped version of the face
#     # Used when perspective changes during rotation
#     return [[self._state[j][i] for j in range(2, -1, -1)] for i in range(2, -1, -1)]