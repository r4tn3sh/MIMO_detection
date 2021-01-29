import numpy as np
from moddemodfunc import normFactor

def getEVM (sampIn, sampOut, mod):
    if sampIn.shape == sampOut.shape:
        err = (sampIn-sampOut)
        evmlin = np.mean(np.square(np.absolute(err)))
        # Since the constellation already has normalized power, no need to
        # further normalize for EVM calculations.
        evm = 10*np.log10(evmlin)
        # There is maximum value of EVM that can be resolved by the signal
        # analyzers in real test environment.
        maxevm = -10*np.log10(normFactor(mod))
        return min(evm, maxevm)
    else:
        print(sampIn.shape, sampOut.shape)
        raise ValueError('size of both parameters should be same')


def getSER (sampIn, sampOut):
    if sampIn.shape == sampOut.shape:
        nofsamp_err = ((sampIn-sampOut)>0).sum(dtype='float')
        return nofsamp_err
    else:
        print(sampIn.shape, sampOut.shape)
        raise ValueError('size of both parameters should be same')
