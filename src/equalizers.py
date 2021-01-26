import math
import numpy as np

from scipy import linalg
from mimoclasses import Equalizer
from mimobasicfunc import *

# ---------- EQUALIZER ------------
def getZfEqualizer(H):
    """
    Generates the zero forcing equalizer for a given channel matrix H.
    """
    if isSquare(H):
        Eq = linalg.inv(H)
    else:
        Eq = linalg.pinv(H)
    return Eq

def getMmseEqualizer(H, Cx, Cz):
    """
    Generates the MMSE equalizer.
    (H_h Cz(-1) H + Cx(-1))(-1) H_h
    Cx = Covariance matrix of i/p signal 'x' across Nt antennas
    Cz = Covariance matrix of noise 'z' across Nr antennas
    """
    Hh = H.conj().T
    tM = Hh*(linalg.inv(Cz)*H) + linalg.inv(Cx)
    return linalg.inv(tM)*Hh

def getEqualizer(H, Cx, Cz, t):
    """
    Main function to generate the channel equalizer.
    """
    print(t)
    if t == Equalizer.ZF:
        Eq = getZfEqualizer(H)
    elif t == Equalizer.MMSE:
        Eq = getMmseEqualizer(H, Cx, Cz)
    else:
        raise ValueError('Choose a valid equalizer type.')
    return Eq
