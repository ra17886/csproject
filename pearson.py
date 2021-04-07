
import os
import json
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb

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

directory = 'pvl_trial'

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



for filename in os.listdir(directory):
    json_file = open(os.path.join(directory, filename),'r')
    data = json.load(json_file)
    getDetails(data)

df = pd.DataFrame(list(zip(age, gender, gad, phq, panasNA, panasPA, trial_length,likelihood, w,a,c)),
               columns =['Age', 'Gender','GAD Score','PHQ Score', "NA Score", "PA Score", "Trial Length","Likelihood","W","A","C"])
pearsoncorr = df.corr(method = 'pearson')
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
plt.savefig('heatmap.png')