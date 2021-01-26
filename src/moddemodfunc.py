import numpy as np

qamcoord = [0, 1, 3, 2, 6, 7, 5, 4,
        12, 13, 15, 14, 10, 11, 9, 8,
        24, 25, 27, 26, 30, 31, 29, 28,
        20, 21, 23, 22, 18, 19, 17, 16] #for max 10 bits

def qammod(b, mod):
    """
    This function takes specific set of bits and maps them into a desired QAM 
    modulation.
    """
    global qamcoord
    if b.size != mod:
        print('number of bits do not match the modulation scheme')
        return -1
    elif mod not in [2, 4, 6, 8, 10]:
        print('Currently supporting only QPSK, 16QAM, 64QAM, 256QAM, 1024QAM')
        return -1
    else:
        dims = np.power(2,mod//2) # one side of the square
        coord = qamcoord[0:dims]
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
