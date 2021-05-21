import os
import json
from wsls_likelihood import computeLikelihood
from scipy.optimize import minimize

"""
finds the most likely parameters by minimises the negative log likelihood in the WSLS model
this is done for each participant as results appended to the participants json and stores in the wsls_trial directory
"""

def saveFile(data, filename):
    n = 'wsls_trial/' + filename
    with open(n, "x") as f:
        json.dump(data,f)
        print('saved ', n)

class F_participant:
    def __init__(self,r,o):
        self.rewards = r
        self.options = o

    def __call__(self):
        p_stay = 0.5
        p_shift = 0.5
        x0 = [p_stay,p_shift]
        #return gridtest.gridtest(self.rewards, self.options)
        return minimize(computeLikelihood,x0, args=(self.rewards, self.options),method = 'Nelder-Mead')

def run_optimiser(r,o):
    f = F_participant(r,o)
    likelihood = f()['fun']
    p_stay = f()['x'][0]
    p_shift = f()['x'][1]

    return likelihood,p_stay,p_shift

directory = 'vse_trial/'

def startOptimiser(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            data['WSLS_likelihood'],data['Shift'], data['Stay']= run_optimiser(data['rewards'],data["options"])
            saveFile(data, filename)

startOptimiser(directory)