import os
import json
import numpy as np

directory = 'evpu_trial/'

#little bit confused on this
def getLikelihoods(directory):
    PVL_Likelihoods = []
    EVPU_Likelihoods = []
    n = 0
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            EVPU_Likelihoods.append(data["EVPU_likelihood"])
            PVL_Likelihoods.append(data["likelihood"])
            n+=1
    return PVL_Likelihoods, EVPU_Likelihoods,n

def LRT(PVL_Likelihoods, EVPU_Likelihoods,n):
    PVL = np.sum(PVL_Likelihoods)
    EVPU = np.sum(EVPU_Likelihoods)

    print("PVL: ", PVL)
    print("EVPU: ", EVPU)

PVL, EVPU,n = getLikelihoods(directory)
LRT(PVL, EVPU,n)

