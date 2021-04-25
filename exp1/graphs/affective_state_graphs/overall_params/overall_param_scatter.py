import numpy as np 
import matplotlib.pyplot as plt
import os
import json

def getScores():
    directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/pvl_trial'
    score = []
    ws = []
    as_ = []
    cs = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            score.append((data['GAD_score']+data['PHQ_score']+data['NA_score']-data['PA_score']))
            ws.append(data["w"])
            as_.append(data["a"])
            cs.append(data["c"])
    return score, ws, as_, cs

def saveScores(score,w,a,c):
    with open("gad_data.txt","w") as f:
        f.write("Score: ")
        for line in score:
            f.write(str(line) + ",")
        f.write(" w:")
        for line in w:
            f.write(str(line) + ",")
        f.write(" a:")
        for line in a:
            f.write(str(line) + ",")
        f.write(" c:")
        for line in c:
            f.write(str(line) + ",")
    f.close()

def scatterW(score,w):
    plt.figure(figsize=[10,8])
    plt.scatter(score, w)
    x = np.array(score)
    y = np.array(w)
    m, b = np.polyfit(x, y, 1)

    plt.plot(x, m*x + b)
    plt.xlabel('Overall Negativity Score')
    plt.ylabel('w')
    plt.title('Overall Negativity Scores')
    plt.show()

def scatterA(score,s):
    plt.figure(figsize=[10,8])
    plt.scatter(score, a)
    x = np.array(score)
    y = np.array(a)
    m, b = np.polyfit(x, y, 1)

    plt.plot(x, m*x + b)
    plt.xlabel('Overall Negativity Score')
    plt.ylabel('a')
    plt.title('Overall Negativity Scores')
    plt.show()

def scatterC(score,c):
    plt.figure(figsize=[10,8])
    plt.scatter(score, c)
    x = np.array(score)
    y = np.array(c)
    m, b = np.polyfit(x, y, 1)

    plt.plot(x, m*x + b)
    plt.xlabel('Overall Negativity Score')
    plt.ylabel('c')
    plt.title('Overall Negativity Scores')
    plt.show()

score, w, a, c = getScores()
saveScores(score,w,a,c)
scatterW(score,w)
scatterA(score,a)
scatterC(score,c)