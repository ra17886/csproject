import os
import json
import numpy as np

directory = 'vse_trial/'


def getLikelihoods(directory):
    PVL_Likelihoods = []
    EVPU_Likelihoods = []
    PVL2_Likelihoods = []
    EVPU2_Likelihoods = []
    VSE_Likelihoods=[]
    n = 0
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            EVPU_Likelihoods.append(data["EVPU_likelihood"])
            PVL_Likelihoods.append(data["likelihood"])
            PVL2_Likelihoods.append(data["PVL2_likelihood"])
            EVPU2_Likelihoods.append(data["EVPU2_likelihood"])
            VSE_Likelihoods.append(data["VSE_likelihood"])
            n+=1
    return PVL_Likelihoods, EVPU_Likelihoods,PVL2_Likelihoods,EVPU2_Likelihoods,VSE_Likelihoods

def LRT(PVL_Likelihoods, EVPU_Likelihoods,PVL2_Likelihoods,EVPU2_Likelihoods,VSE_Likelihoods):
    PVL = np.sum(PVL_Likelihoods)
    EVPU = np.sum(EVPU_Likelihoods)
    PVL2 = np.sum(PVL2_Likelihoods)
    EVPU2 = np.sum(EVPU2_Likelihoods)
    VSE = np.sum(VSE_Likelihoods)

    print("PVL: ", PVL)
    print("EVPU: ", EVPU)
    print("PVL2: ", PVL2)
    print("EVPU2: ",EVPU2)
    print("VSE: ",VSE)

def BIC(PVL_Likelihoods, EVPU_Likelihoods,PVL2_Likelihoods,EVPU2_Likelihoods,VSE_Likelihoods):
    #BIC = -2 * LL + log(N) * k
    PVL = 2*np.sum(PVL_Likelihoods)+(np.log(45))*3
    EVPU = 2*np.sum(EVPU_Likelihoods)+(np.log(45))*3
    PVL2 = 2*np.sum(PVL2_Likelihoods)+(np.log(45))*2
    EVPU2 = 2*np.sum(EVPU2_Likelihoods)+(np.log(45))*2
    VSE = 2*np.sum(VSE_Likelihoods)+(np.log(45))*4
    print("BIC:")
    print("PVL: ", PVL)
    print("EVPU: ", EVPU)
    print("PVL2: ", PVL2)
    print("EVPU2: ",EVPU2)
    print("VSE: ",VSE)

def AIC(PVL_Likelihoods, EVPU_Likelihoods,PVL2_Likelihoods,EVPU2_Likelihoods,VSE_Likelihoods):
    #AIC = -2/N * LL + 2 * k/N
    PVL = 2/45*np.sum(PVL_Likelihoods)+(2*3/45)
    EVPU = 2/45*np.sum(EVPU_Likelihoods)+(2*3/45)
    PVL2 = 2/45*np.sum(PVL2_Likelihoods)+(2*2/45)
    EVPU2 = 2/45*np.sum(EVPU2_Likelihoods)+(2*2/45)
    VSE = 2/45*np.sum(VSE_Likelihoods)+(2*4/45)
    print("AIC:")
    print("PVL: ", PVL)
    print("EVPU: ", EVPU)
    print("PVL2: ", PVL2)
    print("EVPU2: ",EVPU2)
    print("VSE: ",VSE)

PVL, EVPU,PVL2,EVPU2,VSE= getLikelihoods(directory)
AIC(PVL, EVPU,PVL2,EVPU2,VSE)
