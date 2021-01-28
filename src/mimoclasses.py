import math

from dataclasses import dataclass
from enum import Enum
from enum import IntEnum

class Equalizer(Enum):
    ZF = 1
    MMSE = 2

class Channel(IntEnum):
    NONE = 1
    RAND_UNIT = 2 # Completely stochastic
    RAND_UNIT_GOOD = 3
    RAND_UNIT_BAD = 4
    FSPL = 5 # Free space path loss
    RAYLEIGH = 6
    RICIAN = 7

@dataclass
class ChParam:
    samprate: int
    delay: float
    doppler: float
    seed: int
