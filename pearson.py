
import os
import json
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

gad =[]
phq = []
panasNA = []
panasPA = []
trial_length = []

directory = 'options_trial'

def getDetails(data):
    gad.append(int(data['GAD_score']))
    phq.append(int(data['PHQ_score']))
    panasNA.append(int(data['NA_score']))
    panasPA.append(int(data['PA_score']))
    trial_length.append(int(data['length']))

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


length_gad()
length_phq()
length_panasNA()
length_panasPA()
interCorrelations()


