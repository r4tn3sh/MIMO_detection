import numpy as np
from moddemodfunc import normFactor

def getEVM (sampIn, sampOut, mod):
    if sampIn.shape == sampOut.shape:
        err = (sampIn-sampOut)
        evmlin = np.mean(np.square(np.absolute(err)))
        evm = 10*np.log10(evmlin*normFactor(mod))
        print(evmlin,evm, normFactor(mod))
        return evm
    else:
        raise ValueError('size of both parameters should be same')


def getSER (sampIn, sampOut):
    if sampIn.shape == sampOut.shape:
        nofsamp_err = ((sampIn-sampOut)>0).sum(dtype='float')
        return nofsamp_err
    else:
        raise ValueError('size of both parameters should be same')
