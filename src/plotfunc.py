import matplotlib.pyplot as plt
from numpy import array

# ---------- PLOTS ------------
def plotConstell(y):
    """
    Plots the constellation of given samples.
    """
    yr = y.real#[a.real for a in y]
    yi = y.imag#[a.imag for a in y]
    nrow, ncol = y.shape
    #p = plt.figure()
    p, ax = plt.subplots()
    for idx in range(nrow):
        plt.scatter(array(yr[idx]), array(yi[idx]), s=3, label='path '+str(idx+1))
    ax.legend()
    return p
