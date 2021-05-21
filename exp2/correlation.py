import os
import json
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import numpy as np

"""
finding pmcc between variables
"""

age = []
gender =[]
gad =[]
phq = []
panasNA = []
panasPA = []
trial_length = []

PVL_likelihood = []
PVL_w = []
PVL_a = []
PVL_c = []
PVL_shape = []

EVPU_w = []
EVPU_a = []
EVPU_c = []
EVPU_shape = []
EVPU_likelihood = []

VSE_likelihood = []
VSE_alpha = []
VSE_delta = []
VSE_theta = []
VSE_phi = []
VSE_c = []



def getDetails(data):
    age.append(data['age'])
    gender.append(data['gender'])
    gad.append(int(data['GAD_score']))
    phq.append(int(data['PHQ_score']))
    panasNA.append(int(data['NA_score']))
    panasPA.append(int(data['PA_score']))
    trial_length.append(int(len(data['options'])))

    PVL_likelihood.append(data['pvl_likelihood'])
    PVL_w.append(data['pvl_w'])
    PVL_a.append(data['pvl_a'])
    PVL_c.append(data['pvl_c'])
    PVL_shape.append(data['pvl_shape'])

    EVPU_w.append(data['evpu_w'])
    EVPU_a.append(data['evpu_a'])
    EVPU_c.append(data['evpu_c'])
    EVPU_shape.append(data['evpu_shape'])
    EVPU_likelihood.append(data['evpu_likelihood'])

    VSE_likelihood.append(data['vse_likelihood'])
    VSE_alpha.append(data['vse_alpha'])
    VSE_delta.append(data['vse_delta'])
    VSE_theta.append(data['vse_theta'])
    VSE_phi.append(data['vse_phi'])
    VSE_c.append(data['vse_c'])

def length_overall():
    plt.figure(figsize=[10,8])
    plt.scatter(overall,trial_length)
    x = np.array(overall)
    y = np.array(trial_length)
    m, b = np.polyfit(x, y, 1)

    plt.plot(x, m*x + b)
    plt.xlabel('Overall Negativity Score')
    plt.ylabel('trial_length')
    plt.title('Overall Negativity Scores')
    plt.show()

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
    
def heatmaps():

    df3 = pd.DataFrame(list(zip(overall,gad,phq,[-v for v in VSE_likelihood],[-p for p in PVL_likelihood],[-e for e in EVPU_likelihood])),
        columns=["Negativity","GAD-7 Score","PHQ-8 Score","VSE Log Likelihood","PVL Log Likelihood","EV-PU Log Likelihood"])
    pearsoncorr3 = df3.corr(method = 'pearson')
    g = sb.heatmap(pearsoncorr3, 
                xticklabels=pearsoncorr3.columns,
                yticklabels=pearsoncorr3.columns,
                cmap='RdBu_r',
                center =0,
                annot=True,
                linewidth = 0.5,
                square = True
                )
    plt.rcParams['figure.figsize']=(10,10)
    plt.show()

def AIC(PVL,EVPU,VSE):
    #AIC = -2/N * LL + 2 * k/N
    pvl_aic = (np.sum(PVL)/48)+(2*4/48)
    evpu_aic = (np.sum(EVPU)/48)+(2*4/48)
    vse_aic = (np.sum(VSE)/48)+(2*5/48)
    print("PVL: ",pvl_aic)
    print("EVPU: ",evpu_aic)
    print("VSE:",vse_aic)





directory = 'optimise_trial/'
for filename in os.listdir(directory):
    json_file = open(os.path.join(directory, filename),'r')
    data = json.load(json_file)
    getDetails(data)

score = []
overall = []
for i in range(len(gad)):
    score.append(panasNA[i] - panasPA[i])
    overall.append(score[i]+gad[i]+phq[i])


length_overall()
corrPhpa,sigD = pearsonr(trial_length,overall)
print("r:",corrPhpa," sig:", sigD)

AIC(PVL_likelihood,EVPU_likelihood,VSE_likelihood)
print(f"\n")
print(trial_length)



