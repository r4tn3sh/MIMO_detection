import math

from enum import Enum
from enum import IntEnum

class Equalizer(Enum):
    ZF = 1
    MMSE = 2

class Channel(IntEnum):
    NONE = 1
    RAND_UNIT = 2
    RAND_UNIT_GOOD = 3
    RAND_UNIT_BAD = 4
