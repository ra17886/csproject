#import pvl 
import json
w = 1
a = 0.4
c = 3

filename = 'options_trial/clean_05-03-21-153517.json'
json_file = open(filename, 'r')



def getInfo(json_file):
    data = json.load(json_file)
    rewards = [int(x) for x in data['rewards']]
    options = [int(x) for x in data['options']]
    return rewards, options

def computeLikelihood(json_file, w, a, c):
    rewards, options = getInfo(json_file)
    print(options)
    likelihood = [0.25]

    for i in range(len(options)):
        print(i)

    #loop starts here
    #get first reward and pass to pvl
    #pvl should return updated u, ev and prob
    #then get the second option and add corresponding prob to likelihood array


computeLikelihood(json_file, w, a, c)



