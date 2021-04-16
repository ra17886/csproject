import os 
import json
import numpy as np 
from scipy import stats

#Running a T-test between the happiest and unhappiest people
#get top 25% and botton 25% of happiness scores
#bottom is happiest group

directory = "pvl_trial/"
top = dict()
bottom = dict()

def getScore(data):
    return data['NA_score'] + data["PHQ_score"] + data['GAD_score'] - data['PA_score']

def getScores(directory):
    scores = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            scores.append(getScore(data))
   # print(scores)
    return scores

def getPercentiles(scores):
    lp = np.percentile(scores, 25)
    tp = np.percentile(scores, 75) #extracting top 25% and bottom 25% of participants
    #print("Top: ", tp)
   # print("Bottom: " ,lp)
    return lp, tp

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


def t_test(bottom, top):
    top_w = getParams(top,"w")
    bottom_w = getParams(bottom,"w")

    top_a = getParams(top,"a")
    bottom_a = getParams(bottom,"a")

    top_c = getParams(top,"c")
    bottom_c = getParams(bottom,"c")

    print("W_PVL T-Test:", stats.ttest_ind(top_w, bottom_w,equal_var = False))
    print("A_PVL T-Test:", stats.ttest_ind(top_a, bottom_a,equal_var = False))
    print("C_PVL T-Test:", stats.ttest_ind(top_c, bottom_c,equal_var = False))


scores = getScores(directory)
lp, tp = getPercentiles(scores)
bottom, top = getGroups(directory, lp, tp)
t_test(bottom, top)