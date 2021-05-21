import os
import json
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb

"""
computes pcc for affective state and vse paramters
compute p values
creates a seaborn heatmap
"""
age = []
gender =[]
gad =[]
phq = []
panasNA = []
panasPA = []
trial_length = []
likelihood = []
alpha = []
delta = []
phi = []
c = []

def calculateScores():
    score = []
    for i in range(len(gad)):
        score.append(gad[i] + panasNA[i] - panasPA[i] + phq[i])
    return score

def getData(data):
    age.append(data['age'])
    gender.append(data['gender'])
    gad.append(int(data['GAD_score']))
    phq.append(int(data['PHQ_score']))
    panasNA.append(int(data['NA_score']))
    panasPA.append(int(data['PA_score']))
    trial_length.append(int(data['length']))
    likelihood.append(data['VSE_likelihood'])
    alpha.append(data['VSE_alpha'])
    delta.append(data['VSE_delta'])
    phi.append(data['VSE_phi'])
    c.append(data['VSE_c'])

def getFiles(directory):
    for filename in os.listdir(directory):
        json_file = open(os.path.join(directory, filename),'r')
        data = json.load(json_file)
        getData(data)

#https://stackoverflow.com/questions/25571882/pandas-columns-correlation-with-statistical-significance
def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1],10)
    return pvalues

directory = 'vse_trial/'
getFiles(directory)


df = pd.DataFrame(list(zip(age, gender,gad,phq,panasNA,panasPA, trial_length, likelihood,alpha,delta,phi,c)),
               columns =['Age', 'Gender',"GAD","PHQ","NA","PA", "Trial Length","Likelihood","Alpha","Delta","Phi","C"])
print(df)
pearsoncorr = df.corr(method = 'pearson')
print(calculate_pvalues(df))

g = sb.heatmap(pearsoncorr, 
            xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.columns,
            cmap='RdBu_r',
            center =0,
            annot=True,
            linewidth = 0.5,
            square = True
            )
plt.rcParams['figure.figsize']=(10,10)
plt.show()