import os
import json
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd
import seaborn as sb
from scipy.stats import pearsonr
#work out relationship between likelihoods and affective state
#get overall happiness score and plot scatter graph between likelihoods

directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/exp1/wsls_trial/'

def computeScore(d):
    return d['NA_score']+d['PHQ_score']+d['GAD_score']-d['PA_score']

def getData(directory):
    scores = []
    PVL = []
    PVL2 = []
    EVPU = []
    EVPU2 = []
    vse=[]
    wsls = []
    GAD =[]
    PHQ = []
    for filename in os.listdir(directory):
            if filename.endswith(".json"):
                json_file = open(os.path.join(directory, filename),'r')
                data = json.load(json_file)
                scores.append(computeScore(data))
                GAD.append(data['GAD_score'])
                PHQ.append(data['PHQ_score'])
                PVL.append(data['likelihood'])
                PVL2.append(data['PVL2_likelihood'])
                EVPU.append(data['EVPU_likelihood'])
                EVPU2.append(data['EVPU2_likelihood'])
                vse.append(data['VSE_likelihood'])
                wsls.append(data['WSLS_likelihood'])
    return [scores,GAD,PHQ ,PVL, PVL2, EVPU, EVPU2,vse,wsls]

def plot(x,y,y_label):
    plt.figure(figsize=[10,8])
    plt.scatter(x, y)

    nx = np.array(x)
    ny = np.array(y)
    m, b = np.polyfit(nx, ny, 1)

    plt.plot(nx, m*nx + b)
    plt.xlabel('Negativity Scores')
    plt.ylabel(y_label + ' Likelihood')
    plt.title('Negativity Score and ' + y_label +  ' Model Correlation')
    plt.show()


#https://stackoverflow.com/questions/25571882/pandas-columns-correlation-with-statistical-significance
def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1],10)
    return pvalues

data = getData(directory)

df1 = pd.DataFrame(list(zip(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])),
               columns =['Score', 'GAD',"PHQ", "PVL","PVL2","EV-PU","EV-PU2","VSE","WSLS"])
pearsoncorr1 = df1.corr(method = 'pearson')

g = sb.heatmap(pearsoncorr1, 
            xticklabels=pearsoncorr1.columns,
            yticklabels=pearsoncorr1.columns,
            cmap='RdBu_r',
            center =0,
            annot=True,
            linewidth = 0.5,
            square = True
            )
plt.rcParams['figure.figsize']=(10,10)
plt.show()

print(calculate_pvalues(df1))

plot(data[0],data[8],'WSLS')
plot(data[0],data[3],'PVL')
plot(data[0],data[4],'PVL2')
plot(data[0],data[5],'EVPU')
plot(data[0],data[6],'EVPU2')
plot(data[0],data[7],'VSE')



   

