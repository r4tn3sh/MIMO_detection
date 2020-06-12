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

    # ML detection
    z = [constellarr[np.argmin(np.abs(constellarr - y[i]))] for i in range(len(y))]
    return z

def awgnChannel(x,N0):
    # x should be avg unit power
    # - Thermal noise = -174dBm/Hz
    # - Variance N0/2 per real symbol
    Nr = np.random.normal(0, N0/2, x.size)
    Ni = np.random.normal(0, N0/2, x.size)
    return (x+Nr+1j*Ni)

def plotConstell(y):
    yr = [a.real for a in y]
    yi = [a.imag for a in y]
    plt.scatter(yr, yi)
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("N", help="Number of complex samples.",
                    type=int)
    parser.add_argument("mod", help="Number of bits per sample.",
                    type=int, choices=[2,4,6,8,10], metavar='Mod')
    parser.add_argument("--snr", help="Signal to noise ratio (dB).",
                    type=float, nargs='?',default = 10, metavar='SNR')
    args = parser.parse_args()
    N = args.N
    mod = args.mod
    snr = args.snr
    N0 = 1/np.power(10,snr/10)

    # generate the baseband IQ signal
    x = generateIQ(N, mod)
    #plotConstell(x)

    # Sending the signal through baseband channel.
    # The signal x should have unit power.
    y = awgnChannel(x,N0)
    #plotConstell(y)

    z = mlDetectionIQ(y, mod)
    #plotConstell(z)
    print(sum((x-z)>10e-6))
    print('SER = '+str(sum((x-z)>10e-6)/N))

if __name__ == "__main__":
    main()
