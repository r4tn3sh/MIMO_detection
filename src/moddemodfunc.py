import numpy as np


def qammod(b, mod):
    """
    This function takes specific set of bits and maps them into a desired QAM
    modulation.
    Real part : +-1 +-3 +-5 .......
    Imag part : +-1 +-3 +-5 .......
    """
    if b.size != mod:
        print('number of bits do not match the modulation scheme')
        return -1
    elif mod not in [2, 4, 6, 8, 10]:
        print('Currently supporting only QPSK, 16QAM, 64QAM, 256QAM, 1024QAM')
        return -1
    else:
        dims = np.power(2,mod//2) # one side of the square
        #coord = qamcoord[0:dims]
        xdim = 0
        ydim = 0
        for i in range(0, mod//2):
            xdim = xdim+b[i]*np.power(2,i)
            ydim = ydim+b[i+mod//2]*np.power(2,i)
        return np.complex(dims-(2*xdim+1), dims-(2*ydim+1))

def normFactor(mod):
    if mod not in [2, 4, 6, 8, 10]:
        print('Currently supporting only QPSK, 16QAM, 64QAM, 256QAM, 1024QAM')
        return -1
    dims = np.power(2,mod//2)
    ene_sum = 0
    for i in range(0,dims//2):
        for j in range(0, dims//2):
            ene_sum = ene_sum+np.power(2*i+1,2)+np.power(2*j+1,2)
    ene_sum = ene_sum/(np.power(dims,2)//4)
    return ene_sum
