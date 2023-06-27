from vpython import *
from time import *

side = box(color = color.white, length = 1, height = 2, width = 0.1)
sleep(2)
side.rotate(angle = 0.1, axis = vec(0, 0, 1))
sleep(2)
side.color = color.red
sleep(2)
side.pos = vector(1, 1, 1)