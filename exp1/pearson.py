
import os
import json
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb

"""
Gets all the data from the JSONS and puts them into arrays, 
computes the pcc for many paramters and creates heatmaps using seaborn
"""

age = []
gender =[]
gad =[]
phq = []
panasNA = []
panasPA = []
trial_length = []
likelihood = []
w = []
a = []
c = []
EVPU_w = []
EVPU_a = []
EVPU_c = []

directory = 'evpu_trial'

def getDetails(data):
    age.append(data['age'])
    gender.append(data['gender'])
    gad.append(int(data['GAD_score']))
    phq.append(int(data['PHQ_score']))
    panasNA.append(int(data['NA_score']))
    panasPA.append(int(data['PA_score']))
    trial_length.append(int(data['length']))
    likelihood.append(data['likelihood'])
    w.append(data['w'])
    a.append(data['a'])
    c.append(data['c'])
    EVPU_w.append(data['EVPU_w'])
    EVPU_a.append(data['EVPU_a'])
    EVPU_c.append(data['EVPU_c'])



def length_gad():
    corr, sig = pearsonr(trial_length,gad)
    plt.scatter(gad,trial_length)
    plt.xlabel('GAD Scores')
    plt.ylabel('Trial Length')
    plt.show()
    print("length vs gad:", corr, " ", sig)

def length_phq():
    corr,sig = pearsonr(trial_length,phq)
    plt.scatter(phq,trial_length)
    plt.xlabel('PHQ Scores')
    plt.ylabel('Trial Length')
    plt.show()
    print("length vs phq:", corr, " ", sig)

def length_panasNA():
    corr,sig = pearsonr(trial_length,panasNA)
    plt.scatter(phq,trial_length)
    plt.ylabel('Trial Length')
    plt.xlabel('PANAS Negative Affect Scores')
    plt.show()
    print("length vs NA:", corr, " ", sig)

def length_panasPA():
    corr,sig = pearsonr(trial_length,panasPA)
    plt.scatter(phq,trial_length)
    plt.xlabel('PANAS Positive Affect Scores')
    plt.ylabel('Trial Length')
    plt.show()
    print("length vs PA:", corr, " ", sig)

def interCorrelations():
    corrGpa, sigA= pearsonr(gad,panasPA)
    corrGna, sigB = pearsonr(gad,panasNA)
    corrGph,sigC = pearsonr(gad,phq)
    corrPhpa,sigD = pearsonr(phq,panasPA)
    corrPhna,sigE = pearsonr(phq,panasNA)
    print("GAD vs PA:", corrGpa, " ", sigA )
    print("GAD vs NA:", corrGna, " ", sigB )
    print("GAD vs PHQ:", corrGph, " ", sigC )
    print("PHQ vs PA:", corrPhpa, " ", sigD )
    print("PHQ vs NA:", corrPhna, " ", sigE )
    

#https://stackoverflow.com/questions/25571882/pandas-columns-correlation-with-statistical-significance
def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1],10)
    return pvalues


for filename in os.listdir(directory):
    json_file = open(os.path.join(directory, filename),'r')
    data = json.load(json_file)
    getDetails(data)

score = []
for i in range(len(gad)):
    score.append(gad[i] + panasNA[i] - panasPA[i] + phq[i])

interCorrelations()

df = pd.DataFrame(list(zip(age, gender,score, trial_length, w,a,c)),
               columns =['Age', 'Gender',"Score", "Trial Length","PVL W","PVL A","PVL C"])
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
#plt.savefig('heatmap.png')

df1 = pd.DataFrame(list(zip(age, gender,score, trial_length, EVPU_w,EVPU_a,EVPU_c)),
               columns =['Age', 'Gender',"Score", "Trial Length","EV-PU W","EV-PU A","EV-PU C"])
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


