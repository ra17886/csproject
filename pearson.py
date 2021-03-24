
import os
import json
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

gad =[]
phq = []
panasNA = []
panasPA = []
trial_length = []

directory = 'length_trial'

def getDetails(data):
    gad.append(int(data['GAD_score']))
    phq.append(int(data['PHQ_score']))
    panasNA.append(int(data['NA_score']))
    panasPA.append(int(data['PA_score']))
    trial_length.append(int(data['length']))

def length_gad():
    corr,_ = pearsonr(trial_length,gad)
    plt.scatter(gad,trial_length)
    plt.xlabel('GAD Scores')
    plt.ylabel('Trial Length')
    plt.show()
    print("length vs gad:", corr)

def length_phq():
    corr,_ = pearsonr(trial_length,phq)
    plt.scatter(phq,trial_length)
    plt.xlabel('PHQ Scores')
    plt.ylabel('Trial Length')
    plt.show()
    print("length vs phq:", corr)

def length_panasNA():
    corr,_ = pearsonr(trial_length,panasNA)
    plt.scatter(phq,trial_length)
    plt.ylabel('Trial Length')
    plt.xlabel('PANAS Negative Affect Scores')
    plt.show()
    print("length vs NA:", corr)

def length_panasPA():
    corr,_ = pearsonr(trial_length,panasPA)
    plt.scatter(phq,trial_length)
    plt.xlabel('PANAS Positive Affect Scores')
    plt.ylabel('Trial Length')
    plt.show()
    print("length vs PA:", corr)

def interCorrelations():
    corrGpa,_ = pearsonr(gad,panasPA)
    corrGna,_ = pearsonr(gad,panasNA)
    corrGph,_ = pearsonr(gad,phq)
    corrPhpa,_ = pearsonr(phq,panasPA)
    corrPhna,_ = pearsonr(phq,panasNA)
    print("GAD vs PA:", corrGpa)
    print("GAD vs NA:", corrGna)
    print("GAD vs PHQ:", corrGph)
    print("PHQ vs PA:", corrPhpa)
    print("PHQ vs NA:", corrPhna)



for filename in os.listdir(directory):
    json_file = open(os.path.join(directory, filename),'r')
    data = json.load(json_file)
    getDetails(data)


length_gad()
length_phq()
length_panasNA()
length_panasPA()
interCorrelations()


