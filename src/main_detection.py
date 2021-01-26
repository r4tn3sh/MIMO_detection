import os
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

from scipy import linalg
from channels import *
from equalizers import *
from mimoclasses import Equalizer
from mimoclasses import Channel
from mimobasicfunc import *
from plotfunc import *
from moddemodfunc import *
from siggenfunc import *
from detectfunc import *
from measurefunc import *


# ---------- MAIN ------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("N", help="Number of complex samples.",
                    type=int)
    parser.add_argument("mod", help="Number of bits per sample.",
                    type=int, choices=[2,4,6,8,10], metavar='Mod')
    parser.add_argument("--snr", help="Signal to noise ratio (dB).",
                    type=float, nargs='?',default = 10, metavar='SNR')
    parser.add_argument("--Nr", help="Number of RX antennas.",
                    type=int, nargs='?',default = 1, metavar='Nr')
    parser.add_argument("--Nt", help="Number of TX antennas.",
                    type=int, nargs='?',default = 1, metavar='Nt')
    parser.add_argument("--txmode", help="Transmission moTX mode. Use multiple antennas for channel diversity or multiple streams.",
                    type=int, nargs='?', choices=[0,1], default = 0, metavar='TX mode')
    args = parser.parse_args()
    N = args.N
    mod = args.mod
    snr = args.snr
    Nr = args.Nr
    Nt = args.Nt
    tx_mode = args.txmode
    N0 = 1/np.power(10,snr/10)

    if Nt != Nr:
        raise ValueError('Currently only Nr=Nt supported.')

    NoS = min(Nr, Nt) # maximum number of possible streams
    H = generateChMatrix(Nr,Nt,Channel.RAND_UNIT_BAD)
    print('Condition number of the generated channel: '+str(np.linalg.cond(H)))

    # generate the baseband IQ signal
    X = generateIQ(Nt, N, mod, tx_mode)
    #plotConstell(x)

    # Starting with diversity gain
    # NOTE: Replicate same signal on all transmit antennas
    Xin = X#np.asmatrix([x]*Nt)
    Cx = np.var(X)*np.identity(Nt) #all antennas receiving same data
    pltx = plotConstell(Xin)
    plt.title('Transmit signal constellation')


    # Pass through the channel
    Xout = H*Xin
    print('Size of received signal (Nt x N): '+str(Xout.shape))

    # Adding white gaussian noise
    # The signal should have unit power. (?)
    Y = awgnChannel(Xout,N0)
    plty = plotConstell(Y)
    plt.title('Received signal constellation')

    # Covariance matrix of noise. Currently assuming uncorrelated across antennas.
    Cz = np.identity(Nr)

    Eq = getEqualizer(H, Cx, Cz, Equalizer.ZF)
    t_Yhat = Eq*Y

    # NOTE: Following is done assuming all Nt antennas had the same data
    Yhat = np.mean(t_Yhat,0)
    pltyhat = plotConstell(Yhat)
    plt.title('Equalized signal constellation')

    Xrec = mlDetectionIQ(Yhat, mod)
    #plotConstell(Xrec)

    nofsamp_err = getSER(X,Xrec)
    print('SER = '+str(nofsamp_err/N/Nt))
    plt.show()

if __name__ == "__main__":
    main()
