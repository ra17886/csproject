from log_likelihood import computeLikelihood
import gridtest
import os
import json
from scipy.optimize import minimize

def saveFile(data, filename):
    n = 'pvl_trial/' + filename
    with open(n, "x") as f:
        json.dump(data,f)
        print('saved ', n)

class F_participant:
    def __init__(self,r,o):
        self.rewards = r
        self.options = o

    def __call__(self):
        w= 3
        a=0
        c=3
        x0 = [w,a,c]
        #return gridtest.gridtest(self.rewards, self.options)
        return minimize(computeLikelihood,x0, args=(self.rewards, self.options),method = 'Nelder-Mead')

def run_optimiser(r,o,rates):
    f = F_participant(r,o)
    likelihood = f()['fun']
    w = f()['x'][0]
    a = f()['x'][1]
    c = f()['x'][2]
    return likelihood, w, a, c

directory = 'options_trial'
def getFiles(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            f = F_participant(data)
            data['likelihood'], data['w'], data['a'], data['c']= run_optimiser([int(x) for x in data['rewards']],[int(x) for x in data['options']])
            
            saveFile(data, filename)

#getFiles(directory)
        #print("Likelihood: ", f()['fun'], "X: ", [float("{:.5f}".format(v)) for v in f()['x']])
        
    