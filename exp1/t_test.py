import os 
import json
import numpy as np 
from scipy import stats
from statistics import mean, stdev

#Running a T-test between the happiest and unhappiest people
#get top 25% and botton 25% of happiness scores
#bottom is happiest group

directory = "vse_trial/"
top = dict()
bottom = dict()

def getGScore(data):
    return data["GAD_score"]

def getPScore(data):
    return data["PHQ_score"]

def getScore(data):
    return data['NA_score'] + data["PHQ_score"] + data['GAD_score'] - data['PA_score']

def getScores(directory):
    scores = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            scores.append(getScore(data))
    print(scores)
    return scores

def getAlphas(directory):
    scores = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            scores.append(data['VSE_alpha'])
    print([round(score,4) for score in scores])
    return scores

def getGScores(directory):
    scores = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            scores.append(getGScore(data))
    print(scores)
    return scores


def getPScores(directory):
    scores = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            scores.append(getPScore(data))
    print(scores)
    return scores

def getPercentiles(scores):
    lp = np.percentile(scores, 25)
    tp = np.percentile(scores, 75) #extracting top 25% and bottom 25% of participants
    print("Top: ", tp)
    print("Bottom: " ,lp)
    return lp, tp

def getGroups(directory, lp, tp):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            if getScore(data) <lp: bottom[filename] = data
            elif getScore(data)>tp: top[filename] = data
    return bottom, top

def getPGroups(directory, lp, tp):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            if getPScore(data) <lp: bottom[filename] = data
            elif getPScore(data)>tp: top[filename] = data
    return bottom, top

def getGGroups(directory, lp, tp):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            if getGScore(data) <lp: bottom[filename] = data
            elif getGScore(data)>tp: top[filename] = data
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

def alpha_t_test(bottom,top):
    top_w = getParams(top,"VSE_alpha")
    bottom_w = getParams(bottom,"VSE_alpha")
    print("GAD TOP MEAN: ", mean(top_w), "STD:", stdev(top_w))
    print("GAD B MEAN: ", mean(bottom_w), "STD:", stdev(bottom_w))
    print("Alpha VSE T-Test:", stats.ttest_ind(top_w, bottom_w,equal_var = False))



alphas = getAlphas(directory)
print(np.mean(alphas))
print(np.std(alphas))
print(f"\n")
print("PHQ:")
phq_scores = getPScores(directory)
lp, tp = getPercentiles(phq_scores)
bottom, top = getPGroups(directory, lp, tp)
alpha_t_test(bottom, top)
print(f"\n")


gad_scores = getGScores(directory)
lp, tp = getPercentiles(gad_scores)
bottom, top = getGGroups(directory, lp, tp)
alpha_t_test(bottom, top)