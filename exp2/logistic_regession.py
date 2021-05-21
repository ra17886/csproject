
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json 
import os
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import numpy as np
from statistics import mean , stdev

"""
this does not do logistic regression

it looks at the box rates in the igt task and correlates them with affective state scores
"""

gad = []
phq = []
panas = []
overall= []
trial_length = []
rates = []
frequent = []
infrequent = []
good = []
bad = []
a_rates = []
b_rates = []
c_rates = []
d_rates = []
evpu_likelihood = []
pvl_likelihood = []


def calculateRates(options,length):
    a = options.count(0)/length
    b = options.count(1)/length
    c = options.count(2)/length
    d = options.count(3)/length

    rates =[a,b,c,d]
    return(rates)

def calculateFreuqencyPreference(rates):
    frequent.append(rates[0]+rates[2])
    infrequent.append(rates[1]+rates[3])

    good.append(rates[2]+rates[3])
    bad.append(rates[0]+rates[1])

def getData(data):
    gad.append(int(data['GAD_score']))
    phq.append(int(data['PHQ_score']))
    panas.append(int(data['NA_score']-int(data['PA_score'])))
    overall.append(int(data['GAD_score'])+int(data['PHQ_score'])+int(data['NA_score']-int(data['PA_score'])))
    trial_length.append(int(len(data['options'])))
    rate_array = calculateRates(data['options'],int(len(data['options'])))
    rates.append(rate_array)
    calculateFreuqencyPreference(rate_array)
    evpu_likelihood.append(data['evpu_likelihood'])
    pvl_likelihood.append(data['pvl_likelihood'])

    return(calculateRates(data['options'],int(len(data['options']))))


def getFiles(directory):
    for filename in os.listdir(directory):
        json_file = open(os.path.join(directory, filename),'r')
        data = json.load(json_file)
        r = getData(data)

#https://stackoverflow.com/questions/25571882/pandas-columns-correlation-with-statistical-significance
def calculate_pvalues(df):
    df = df.dropna()._get_numeric_data()
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1],10)
    return pvalues

def heatmap():
   
     df1 = pd.DataFrame(list(zip(overall,panas,gad,phq,trial_length,a_rates,b_rates,c_rates,d_rates,good,bad,frequent,infrequent)),
                columns =["Overall","PANAS","GAD","PHQ","Length","A","B","C","D","good","bad","freq","infreq"])
     pearsoncorr1 = df1.corr(method = 'pearson')

     print(calculate_pvalues(df1))
     
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

def stats():
    #heatmap()
    plt.figure(figsize=[10,8])
    plt.scatter(gad, frequent)
    x = np.array(gad)
    y = np.array(frequent)
    m, b = np.polyfit(x, y, 1)

    plt.plot(x, m*x + b)
    plt.xlabel('Gad')
    plt.ylabel('frequent')
    plt.title('Preference for frequent decks with anxiety')
    plt.show()


directory = 'optimise_trial'
getFiles(directory)
for i in range(len(rates)):
    a_rates.append(rates[i][0])
    b_rates.append(rates[i][1])
    c_rates.append(rates[i][2])
    d_rates.append(rates[i][3])


#plt.rcdefaults()
#fig, ax = plt.subplots()


#boxes = ('A', 'B', 'C', 'D')
#y_pos = np.arange(len(boxes))
#performance = [mean(a_rates),mean(b_rates),mean(c_rates),mean(d_rates)]
#error = [stdev(a_rates),stdev(b_rates),stdev(c_rates),stdev(d_rates)]

#ax.barh(y_pos,performance, xerr=error, align='center')
#ax.set_yticks(y_pos)
#ax.set_yticklabels(boxes)
#ax.invert_yaxis()  # labels read top-to-bottom
#ax.set_xlabel('Box Rates')
#ax.set_title('Rates for each box')

#plt.show()

print(good)
print(bad)

plt.scatter(good,evpu_likelihood)
plt.xlabel("good preference")
plt.ylabel("evpu_likelihood")
plt.show()

plt.scatter(good,pvl_likelihood)
plt.xlabel("good preference")
plt.ylabel("pvl_likelihood")
plt.show()