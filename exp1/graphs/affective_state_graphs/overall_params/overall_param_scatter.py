import numpy as np 
import matplotlib.pyplot as plt
import os
import json
import pandas as pd 
import seaborn as sns
import statistics 



def getScores():
    directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/exp1/wsls_trial'
    score = []
    PANAS_n = []
    GAD_n = []
    PHQ_n = []

    GAD = []
    PHQ = []
    length = []

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            score.append((data['GAD_score']+data['PHQ_score']+data['NA_score']-data['PA_score']))
            PANAS_n.append((data['NA_score']-data['PA_score'])/10 + 5)
            GAD_n.append(data['GAD_score']/2.1)
            PHQ_n.append(data['PHQ_score']/2.4)
            GAD.append(data['GAD_score'])
            PHQ.append(data['PHQ_score'])
            length.append(len(data['options']))
    return score, GAD, PHQ, length

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

def GAD_severity(gad):
    none = []
    mild = []
    moderate = []
    severe = []

    for g in gad:
        print(g)
        if g>15: severe.append(g)
        elif g>10: moderate.append(g)
        elif g>5: mild.append(g)
        elif g>-1: none.append(g)

    print(len(gad))
    print("none: ",len(none))
    print("mild: ",len(mild))
    print("moderate: ",len(moderate))
    print("severe: ",len(severe))

def phq_severity(phq):
    none = []
    mild = []
    moderate = []
    moderate_severe = []
    severe = []

    for g in phq:
        print(g)
        if g>20: severe.append(g)
        if g>15: moderate_severe.append(g)
        elif g>10: moderate.append(g)
        elif g>5: mild.append(g)
        elif g>-1: none.append(g)

    print(len(phq))
    print("none: ",len(none))
    print("mild: ",len(mild))
    print("moderate: ",len(moderate))
    print("moderately severe:",len(moderate_severe))
    print("severe: ",len(severe))

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

def scatterLength(phq,length):
    plt.figure(figsize=[10,8])
    plt.scatter(score, length)
    x = np.array(score)
    y = np.array(length)
    m, b = np.polyfit(x, y, 1)

    plt.plot(x, m*x + b)
    plt.xlabel('Overall Negativity Score')
    plt.ylabel('Trial Length')
    plt.title('Trial Length by Negativity Scores')
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

def scatterC(phq,c):
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

score, gad, phq, length = getScores()


print(max(score))
print(min(score))
print(mean(score))

#saveScores(score,w,a,c)
#scatterW(score,w)
#scatterA(score,a)
#scatterC(score,c)

#df = pd.DataFrame(score,columns=['Negativity Scores'])
#ax = sns.distplot(df, hist=True, kde=True,bins=20,
       #       color = 'darkblue', 
       #      hist_kws={'edgecolor':'black'},
       #      kde_kws={'linewidth': 4});
#plt.title("Overall Negativity Scores")
#plt.xlabel("Negativity Score")
#plt.show()

#df = pd.DataFrame(list(zip(gad,phq,panas)),columns=['GAD Scores','PHQ Scores','PANAS Scores'])

#sns.set_style('whitegrid')
#ax= sns.stripplot(data=df)
#ax= sns.boxplot(data=df)
#plt.title('Spread of Affective State Scores')
#plt.show()


