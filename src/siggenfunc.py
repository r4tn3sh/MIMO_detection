from moddemodfunc import *

def generateIQ(Nt, N, mod, tx_mode):
    # Nt = no. of antennas
    # N = number of samples
    # mod = modulation scheme, BPSK, QPSK, ..., 1024QAM
    #   BPSK=1, QPSK=2, ... 1024QAM=10
    # TODO: improve the time-consuming loop
    c = np.asmatrix([[np.complex(0,0)]*N]*Nt)
    if tx_mode == 0: #sending same data in all antennas
        for j in range(N):
            # get random bits
            b = np.random.randint(2, size=mod)
            # encode bits into samples
            temp_c = qammod(b, mod)
            for i in range(Nt):
                c[i,j] = temp_c
    elif tx_mode == 1: #sending different data in each antenna
        for i in range(Nt):
            for j in range(N):
                # get random bits
                b = np.random.randint(2, size=mod)
                # encode bits into samples
                c[i,j] = qammod(b, mod)
    # Normalize the signal to unit power
    c = c/np.sqrt(normFactor(mod))
    return c
