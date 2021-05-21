import os
import json
from scipy.optimize import minimize
import log_likelihood as ll

"""
optimises for the wsls model, this model was not analysed for the thesis
"""

def saveFile(data, filename):
    n = 'final_trial/' + filename
    with open(n, "x") as f:
        json.dump(data,f)
        print('saved ', n)

class F_participant:
    def __init__(self,r,o,p):
        self.rewards = r
        self.options = o
        self.penalties = p

    def __call__(self):
        p_stay = 0.5
        p_shift = 0.5
        wsls0 = [p_stay,p_shift]
        totals = []
        #return gridtest.gridtest(self.rewards, self.options)
        for i in range(len(self.penalties)):
            totals.append(self.rewards[i]-self.penalties[i])
        wsls = minimize(ll.computeLikelihoodWSLS,wsls0,args=(totals, self.options),method = 'Nelder-Mead')
        return wsls

def extract_values(data):
    return [data['fun'],data['x']]
    

    
def run_optimiser(r,o,p):
    f = F_participant(r,o,p)
    wsls_values = f()
    wsls = extract_values(wsls_values)
    return wsls

directory = 'optimise_trial/'

def startOptimiser(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            wsls = run_optimiser(data['rewards'],data["options"],data["penalties"])

            data["wsls_likelihood"] = wsls[0]
            data["p_stay"] = wsls[1][0]
            data["p_shift"] = wsls[1][1]

            print(filename)
            saveFile(data, filename)

startOptimiser(directory)
