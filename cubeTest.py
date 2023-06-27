from DisplayCube3 import *
from Cube3 import *
from Cube3Util import *

stateStrs = []
stateStrs.append("rbwyywogr yryorygyg bgbogoybw orwwowgyb grbrbbrgy rboowwwgo")
stateStrs.append("wbwrwrygr goyygywwg bbrbrbywy bobwbybrg owrgoowro googygryo")
stateStrs.append("ywygrwrww wbogwbwbg ggrrgbwgo gobyyryog robybryrb oorwoyoyb")
stateStr = stateStrs[0].replace(' ', '')
cube = Cube3(parseCube3State(stateStr))
display = DisplayCube3(cube)
cube.solve()