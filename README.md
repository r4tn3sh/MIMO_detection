# MIMO Wireless Communication
## Description
The goal of this project is to create a simulation of a basic baseband communication with MIMO using Python. The following sub-goals are expected to be achieved.
* Bits to sample mapping based on the modulation scheme. Currently supporting BPSK, QPSK, 16QAM, 64QAM, 256QAM, and 1024QAM.
* Modeling various channel matrices, H.
* Implementation of AWGN channel.
* Channel estimation algorithms.
* Sample detection algorithms.
* Useful plotting capability
  * Time and frequency domain representation
  * Constellation 

## Currently implemented
* Channels:
    * AWGN
    * Random fading channel based on condition number
* Equalizer: Zero-Forcing, MMSE


## Required Python libraries:
* Numpy
* Matplotlib
* Argparse
* Enum
