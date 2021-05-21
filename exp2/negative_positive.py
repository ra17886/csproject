import json 
import os
import numpy as np 
import matplotlib.pyplot as plt 
from statistics import mean, stdev
from scipy import stats

top = dict()
bottom = dict()

"""
The code used for T Testing in the IGT 
"""


def getPercentiles(scores):
    lp = np.percentile(scores, 25)
    tp = np.percentile(scores, 75) #extracting top 25% and bottom 25% of participants
    print("Top: ", tp)
    print("Bottom: " ,lp)
    return lp, tp


def getScore(d):
    return d['NA_score']+d['PHQ_score']+d['GAD_score']-d['PA_score']

def getGroups(directory, lp, tp):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            if getScore(data) <lp: bottom[filename] = data
            elif getScore(data)>tp: top[filename] = data
    return bottom, top

def getParams(data,param):
    ps = []
    for item in data:
        p = data[item]
        ps.append(p[param])
    return ps

def getScores(data):
    gads = getParams(data,"GAD_score")
    phqs = getParams(data,"PHQ_score")
    nas = getParams(data,"NA_score")
    pas = getParams(data,"PA_score")

    score = []
    for i in range(len(gads)):
        score.append(gads[i]+phqs[i]+nas[i]-pas[i])
    return score

def getData(directory):
    scores = []
    w = []
    GAD =[]
    PHQ = []
    a = []
    c = []
    shape = []

    for filename in os.listdir(directory):
            if filename.endswith(".json"):
                json_file = open(os.path.join(directory, filename),'r')
                data = json.load(json_file)
                scores.append(getScore(data))
                w.append(data['pvl_w'])
                a.append(data['pvl_a'])
                c.append(data['pvl_c'])
                shape.append(data['pvl_shape'])
    return scores,w,a,c,shape

directory = 'optimise_trial'
scores, w, a, c, shape = getData(directory)
lp, tp = getPercentiles(scores)
bottom, top = getGroups(directory,lp,tp)

tops = [getParams(top,"pvl_w"),getParams(top, "pvl_a"),getParams(top,"pvl_c"),getParams(top,"pvl_shape")]
top_scores = getScores(top)
top_means = [mean(x) for x in tops]
top_stds = [stdev(x) for x in tops]

bottoms = [getParams(bottom,"pvl_w"),getParams(bottom, "pvl_a"),getParams(bottom,"pvl_c"),getParams(bottom,"pvl_shape")]
bottom_scores = getScores(bottom)
bottom_means = [mean(x) for x in bottoms]
bottom_stds = [stdev(x) for x in bottoms]

top_length = [len(x) for x in getParams(top,"options")]
bottom_length = [len(x) for x in getParams(bottom,"options")]

for i in range(4):
    print(stats.ttest_ind(tops[i],bottoms[i]))



labels = ['PVL W *', 'PVL A','PVL C', 'PVL Shape']
x = np.arange(len(labels))  
width = 0.35 

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, top_means, width,label='Least Happy')
rects2 = ax.bar(x + width/2, bottom_means, width,label='Most Happy')

ax.set_ylabel('Parameter Value')
ax.set_title('Parameter Values by Negativity Scores')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


fig.tight_layout()

plt.show()