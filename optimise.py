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
    def __init__(self,data):
        self.rewards = [int(x) for x in data['rewards']]
        self.options = [int(x) for x in data['options']]
        self.age = data['age']
        self.gender = data['gender']
        self.NA = data['NA_score']
        self.PA = data['PA_score']
        self.PHQ = data['PHQ_score']
        self.GAD = data['GAD_score']
    def __call__(self):
        w= 0
        a=0
        c=0
        x0 = [w,a,c]
        #return gridtest.gridtest(self.rewards, self.options)
        return minimize(computeLikelihood,x0, args=(self.rewards, self.options),method = 'Nelder-Mead')

directory = 'options_trial'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        json_file = open(os.path.join(directory, filename),'r')
        data = json.load(json_file)
        f = F_participant(data)
        data['likelihood']=f()['fun']
        data['w']=f()['x'][0]
        data['a']=f()['x'][1]
        data['c']=f()['x'][2]
        
        saveFile(data, filename)

        #print("Likelihood: ", f()['fun'], "X: ", [float("{:.5f}".format(v)) for v in f()['x']])
        
    