import matplotlib.pyplot as plt 
import os
import json
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

directory = 'exp1/model_accuracy'

"""
plots the param_accuracy graphs using the parametry recovery data, this is for exp 1
"""
def getError(true, estimated):
    errs = []
    for i in range(len(true)):
        errs.append(true[i]-estimated[i])
    return errs

def getValues(parameter):
    true = []
    estimated = []
    for filename in os.listdir(directory):
        json_file = open(os.path.join(directory, filename),'r')
        data = json.load(json_file)
        true.append(data[parameter]["actual"])
        estimated.append(data[parameter]["estimate"])
    return getError(true,estimated)

def plot(n,errors,range,label):
    N, bins, patches = axs[n].hist(errors, bins=n_bins,range = (range[0],range[1]))
    fracs = N / N.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    axs[n].set_xlabel(label)
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)


w_errors = getValues('PVL_w')
a_errors = getValues('PVL_a')
c_errors = getValues('PVL_c')

alpha_errs = getValues('VSE_alpha')
delta_errs = getValues('VSE_delta')
phi_errs = getValues('VSE_phi')
c_errs = getValues('VSE_c')

fig, axs = plt.subplots(1, 4, sharey=True, tight_layout=True)
n_bins = 10


plot(0,delta_errs,[-1,1],"VSE Delta")
plot(1,alpha_errs,[-1,1], "VSE Alpha")
plot(2,phi_errs,[-10,10], "VSE Phi")
plot(3,c_errs,[-1,1], "VSE C")

plt.show()