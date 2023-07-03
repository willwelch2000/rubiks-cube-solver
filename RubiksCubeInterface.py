from DisplayRubiksCube import *
from RubiksCube import *
from RubiksCubeUtil import *

needExplanationString = "Do you need an explanation? (y/n)\n"
needExplanation = input(needExplanationString).lower() in ['y', 'yes']
explanation = '''Enter the state of the Rubik's Cube in the following format:
    Enter each face in the order: top, front, right, back, left, bottom
        The top, bottom, right, and left are all oriented by moving one 90-degree rotation from the front
        The back is oriented by rotating from the front to the right face and then to the back
    
    For each face, enter nine characters representing the colors of the squares on the face (r, g, b, w, y, o)
        Go in the order: top row, middle row, bottom row
        
    White space is allowed anywhere to make more readable'''
if needExplanation:
    print(explanation)
else:
    print("Enter the state:")

stateStr = input().replace(' ', '')
cube = RubiksCube(parseRubiksCubeState(stateStr))
display = DisplayRubiksCube(cube)

if cube.solve():
    print("Complete! Enter 'stop' to end program.")
else:
    print("Failed to solve. You likely entered an illegal cube setup.")
    
while input("") != "stop":
    pass