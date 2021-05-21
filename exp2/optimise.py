import os
import json
from scipy.optimize import minimize
import log_likelihood as ll

"""
optimisation for all three models
"""
def saveFile(data, filename):
    n = 'optimise_trial/' + filename
    with open(n, "x") as f:
        json.dump(data,f)
        print('saved ', n)

class F_participant:
    def __init__(self,r,o,p):
        self.rewards = r
        self.options = o
        self.penalties = p

    def __call__(self):
        delta = 0
        alpha = 0
        phi = 0
        c = 0
        theta = 0
        w = 0
        a = 0
        shape = 0
        pvl0 = [w,a,c,shape]
        evpu0=[w,a,c,shape]
        vse0 = [delta,alpha,phi,c,theta]
        #return gridtest.gridtest(self.rewards, self.options)
        pvl = minimize(ll.computeLikelihoodPVL,pvl0, args=(self.rewards, self.options, self.penalties),method = 'Nelder-Mead')
        evpu = minimize(ll.computeLikelihoodEVPU,evpu0,args=(self.rewards,self.options,self.penalties),method = "Nelder-Mead")
        vse = minimize(ll.computeLikelihoodVSE,vse0,args=(self.rewards, self.options, self.penalties),method = 'Nelder-Mead')
        return pvl,evpu,vse

def extract_values(data):
    return [data['fun'],data['x']]
    

    
def run_optimiser(r,o,p):
    f = F_participant(r,o,p)
    pvl_values, evpu_values, vse_values = f()
    pvl = extract_values(pvl_values)
    evpu = extract_values(evpu_values)
    vse = extract_values(vse_values)
    return pvl, evpu, vse

directory = 'trial/'

def startOptimiser(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            pvl, evpu,vse = run_optimiser(data['rewards'],data["options"],data["penalties"])

            data["pvl_likelihood"] = pvl[0]
            data["pvl_w"] = pvl[1][0]
            data["pvl_a"] = pvl[1][1]
            data["pvl_c"] = pvl[1][2]
            data["pvl_shape"] = pvl[1][3]

            data["evpu_likelihood"] = evpu[0]
            data["evpu_w"] = evpu[1][0]
            data["evpu_a"] = evpu[1][1]
            data["evpu_c"] = evpu[1][2]
            data["evpu_shape"] = evpu[1][3]

            data["vse_likelihood"] = vse[0]
            data["vse_delta"] = vse[1][0]
            data["vse_alpha"] = vse[1][1]
            data["vse_phi"] = vse[1][2]
            data["vse_c"] = vse[1][3]
            data["vse_theta"] = vse[1][4]

            print(filename)

            saveFile(data, filename)

startOptimiser(directory)
