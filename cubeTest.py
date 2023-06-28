from DisplayCube3 import *
from Cube3 import *
from Cube3Util import *

stateStrs = []
stateStrs.append("rbwyywogr yryorygyg bgbogoybw orwwowgyb grbrbbrgy rboowwwgo")
stateStrs.append("wbwrwrygr goyygywwg bbrbrbywy bobwbybrg owrgoowro googygryo")
stateStrs.append("ywygrwrww wbogwbwbg ggrrgbwgo gobyyryog robybryrb oorwoyoyb")
stateStrs.append("ygrrywyoo bwwgbwyrg bgbrrywbr wyrogrboo gbogoowyg oyrbwwgby")
stateStr = stateStrs[3].replace(' ', '')
cube = Cube3(parseCube3State(stateStr))
display = DisplayCube3(cube)
cube.solve()
print("Complete! Enter 'stop' to end program.")
while input("") != "stop":
    pass