from DisplayRubiksCube import *
from RubiksCube import *
from RubiksCubeUtil import *

stateStrs = []
stateStrs.append("rbwyywogr yryorygyg bgbogoybw orwwowgyb grbrbbrgy rboowwwgo")
stateStrs.append("wbwrwrygr goyygywwg bbrbrbywy bobwbybrg owrgoowro googygryo")
stateStrs.append("ywygrwrww wbogwbwbg ggrrgbwgo gobyyryog robybryrb oorwoyoyb")
stateStrs.append("ygrrywyoo bwwgbwyrg bgbrrywbr wyrogrboo gbogoowyg oyrbwwgby")
stateStrs.append("oyryowboy obgrworyo ogbwbwwrr wrwbyyboy bbyggbggw gogrrwrgy")
stateStr = stateStrs[0].replace(' ', '')
cube = RubiksCube(parseRubiksCubeState(stateStr))
display = DisplayRubiksCube(cube)
cube.solve()
print("Complete! Enter 'stop' to end program.")
while input("") != "stop":
    pass