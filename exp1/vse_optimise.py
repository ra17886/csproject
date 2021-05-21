import os
import json
from vse_likelihood import computeLikelihood
from scipy.optimize import minimize

"""
optimisation for the vse model
"""

def saveFile(data, filename):
    n = 'vse_trial/' + filename
    with open(n, "x") as f:
        json.dump(data,f)
        print('saved ', n)

class F_participant:
    def __init__(self,r,o):
        self.rewards = r
        self.options = o

    def __call__(self):
        delta = 0
        alpha = 0
        phi = 0
        c = 0
        x0 = [delta,alpha,phi,c]
        #return gridtest.gridtest(self.rewards, self.options)
        return minimize(computeLikelihood,x0, args=(self.rewards, self.options),method = 'Nelder-Mead')

def run_optimiser(r,o):
    f = F_participant(r,o)
    likelihood = f()['fun']
    delta = f()['x'][0]
    alpha = f()['x'][1]
    phi = f()['x'][2]
    c = f()['x'][3]
    return likelihood,delta,alpha,phi,c

directory = 'evpu2_trial/'

def startOptimiser(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            data['VSE_likelihood'],data['VSE_delta'], data['VSE_alpha'],data['VSE_phi'],data['VSE_c']= run_optimiser(data['rewards'],data["options"])
            saveFile(data, filename)

#startOptimiser(directory)