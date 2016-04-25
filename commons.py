# All the constants here are meant to be used by
# from commons import *

PAGE_PROGRAMMED, PAGE_ERASED = 'PAGE_PROGRAMMED', 'PAGE_ERASED'

BYTE, KB, MB, GB, TB = [2**(10*i) for i in range(5)]

# unit is based on nanoseconds
SEC, MILISEC, MICROSEC, NANOSEC = [ 1000**3, 1000**2, 1000, 1 ]
# SEC, MILISEC, MICROSEC, NANOSEC = [ 1.0, 0.001, 0.000001, 0.000000001 ]

OP_READ, OP_WRITE, OP_ERASE = 'OP_READ', 'OP_WRITE', 'OP_ERASE'

TAG_BACKGROUND = "BACKGROUND"
TAG_FOREGROUND = "FOREGROUND"

