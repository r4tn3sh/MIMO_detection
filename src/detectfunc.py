import numpy as np
from moddemodfunc import normFactor

def mlDetectionIQ(y, mod):
    # y = complex signal
    # mod = modulation scheme, BPSK, QPSK, ..., 1024QAM
    #   BPSK=1, QPSK=2, ... 1024QAM=10
    dims = np.power(2,mod//2) # one side of the square
    constellind = [2*x-dims+1 for x in range(dims)]/np.sqrt(normFactor(mod))
    constellarr = [np.complex(constellind[i], constellind[j]) for i in range(dims) for j in range(dims)]

    # Maximum Likerlihood detection
    #z = [constellarr[np.argmin(np.abs(constellarr - y[i]))] for i in range(len(y))]
    z = [constellarr[np.argmin(np.abs(constellarr - x))] for x in np.nditer(y)]
    return np.asmatrix(z).reshape(y.shape)
