import os
import math
import numpy as np

# ---------- CHANNEL ------------
def awgnChannel(x,N0):
    # x should be avg unit power
    # - Thermal noise = -174dBm/Hz
    # - Variance N0/2 per real symbol
    N0_r = np.random.normal(0, N0/2, x.shape)
    N0_i = np.random.normal(0, N0/2, x.shape)
    return (x+N0_r+1j*N0_i)

NO_CHANNEL = 0
RAND_UNIT_CHANNEL = 1
def generateChMatrix(Nr,Nt,chtype):
    # TODO: support different channel models in future.
    if chtype == NO_CHANNEL:
        if Nr==Nt:
            H_r = np.identity(Nr)
            H_i = np.zeros((Nr,Nt))
        else:
            raise ValueError('For channel type-'+str(chtype)+', Nr=Nt is needed.')
            return -1
    elif chtype == RAND_UNIT_CHANNEL:
        # Using complex gaussian random variable
        # Real and Img part: mean = 0, variance = 1
        H_r = np.random.normal(0, 1, size=(Nr,Nt))
        H_i = np.random.normal(0, 1, size=(Nr,Nt))
    else:
        raise ValueError('Channel type-'+str(chtype)+' is not supported.')
        return -1

    return np.asmatrix((H_r + 1j*H_i))

