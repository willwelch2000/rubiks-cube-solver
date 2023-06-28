from DisplayCube3 import *
from Cube3 import *
from Cube3Util import *

needExplanationString = "Do you need an explanation? (y/n)\n"
needExplanation = input(needExplanationString).lower() in ['y', 'yes']
explanation = '''Enter the state of the Rubik's Cube in the following format:
    Enter each face in the order: top, front, right, back, left, bottom
        The top, bottom, right, and left are all oriented by moving one 90-degree rotation from the front
        The back is oriented by rotating from the front to the right face and then to the back
    
    For each face, enter nine characters representing the colors of the squares on the face (r, g, b, w, y, o)
        Go in the order: top row, middle row, bottom row
        
    White space is allowed anywhere to make more readable
'''
if needExplanation:
    print(explanation)
else:
    print("Enter the state:\n")

stateStr = input().replace(' ', '')
cube = Cube3(parseCube3State(stateStr))
display = DisplayCube3(cube)
cube.solve()
print("Complete! Enter 'stop' to end program.")
while input("") != "stop":
    pass