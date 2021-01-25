import matplotlib.pyplot as plt

# ---------- PLOTS ------------
def plotConstell(y):
    yr = [a.real for a in y]
    yi = [a.imag for a in y]
    p = plt.figure()
    plt.scatter(yr, yi,s=3)
    return p
