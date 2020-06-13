import os
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

qamcoord = [0, 1, 3, 2, 6, 7, 5, 4,
        12, 13, 15, 14, 10, 11, 9, 8,
        24, 25, 27, 26, 30, 31, 29, 28,
        20, 21, 23, 22, 18, 19, 17, 16] #for max 10 bits

# This function takes specific set of bits and maps them
# into a desired QAM modulation.
def qammod(b, mod):
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


def generateIQ(N, mod):
    # N = number of samples
    # mod = modulation scheme, BPSK, QPSK, ..., 1024QAM
    #   BPSK=1, QPSK=2, ... 1024QAM=10
    bitN = N * mod
    c = [np.complex(0,0)]*N
    for i in range(N):
        # get random bits
        b = np.random.randint(2, size=mod)
        # encode bits into samples
        c[i] = qammod(b, mod)
    # Normalize the signal to unit power
    c = c/np.sqrt(normFactor(mod))
    return c

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
        # Real and Img part: mean = 1, variance = 1
        H_r = np.random.normal(1, 1, size=(Nr,Nt))
        H_i = np.random.normal(1, 1, size=(Nr,Nt))
    else:
        raise ValueError('Channel type-'+str(chtype)+' is not supported.')
        return -1

    return np.asmatrix((H_r + 1j*H_i))


# ---------- PLOTS ------------
def plotConstell(y):
    yr = [a.real for a in y]
    yi = [a.imag for a in y]
    plt.scatter(yr, yi,s=3)
    plt.show()


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
    args = parser.parse_args()
    N = args.N
    mod = args.mod
    snr = args.snr
    Nr = args.Nr
    Nt = args.Nt
    N0 = 1/np.power(10,snr/10)

    NoS = min(Nr, Nt) # maximum number of possible streams
    H = generateChMatrix(Nr,Nt,NO_CHANNEL)

    # generate the baseband IQ signal
    x = generateIQ(N, mod)

    # Starting with diversity gain
    # Replicate same signal on all transmit antennas
    Xin = np.asmatrix([x]*Nt)
    #plotConstell(Xin)

    # Sending the signal through baseband channel.
    # The signal x should have unit power.
    y = awgnChannel(Xin,N0)
    plotConstell(y)

    z = mlDetectionIQ(y, mod)
    #plotConstell(z)

    nofsamp_err = ((Xin-z)>10e-6).sum(dtype='float')
    print(nofsamp_err)
    print('SER = '+str(nofsamp_err/N))

if __name__ == "__main__":
    main()
