import json 
import os
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
from statistics import mean, stdev
from scipy import stats 

"""
basic demographic calculations for things like affective state severity, age and gender
"""

age = []
gender =[]
gad =[]
phq = []
panasNA = []
panasPA = []
trial_length = []
likelihood = []
length = []
scores = []
panas = []
PANAS_n = []
GAD_n = []
options = []
PHQ_n = []

def getData(data):
    age.append(data['age'])
    gender.append(data['gender'])
    gad.append(int(data['GAD_score']))
    phq.append(int(data['PHQ_score']))
    panasNA.append(int(data['NA_score']))
    panasPA.append(int(data['PA_score']))
    panas.append(int(data['NA_score'])-int(data['PA_score']))
    trial_length.append(int(len(data['options'])))
    length.append(int(data['length']))
    PANAS_n.append((data['NA_score']-data['PA_score'])/10 + 5)
    GAD_n.append(data['GAD_score']/2.1)
    PHQ_n.append(data['PHQ_score']/2.4)
    options.append(data['options'])

def calculateScores():
       for i in range(len(gad)):
              scores.append(gad[i]+phq[i]+panasNA[i]-panasPA[i])
              panas.append(panasNA[i]-panasPA[i])

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


directory = 'optimise_trial'

def getFiles(directory):
    for filename in os.listdir(directory):
        json_file = open(os.path.join(directory, filename),'r')
        data = json.load(json_file)
        getData(data)

getFiles(directory)
age_count = {}
for element in age:
   # checking whether it is in the dict or not
   if element in age_count:
      # incerementing the count by 1
      age_count[element] += 1
   else:
      # setting the count to 1
      age_count[element] = 1
# printing the elements frequencies
for key, value in age_count.items():
   print(f"{key}: {value}")

gender_count = {}
for element in gender:
   # checking whether it is in the dict or not
   if element in gender_count:
      # incerementing the count by 1
      gender_count[element] += 1
   else:
      # setting the count to 1
      gender_count[element] = 1
# printing the elements frequencies
for key, value in gender_count.items():
   print(f"{key}: {value}")

print("gad", mean(GAD_n))
print("phq",mean(PHQ_n))
print("panas",mean(PANAS_n))

#df = pd.DataFrame(list(zip(GAD_n,PHQ_n,PANAS_n)),columns=['Normalised GAD Scores','Normalised PHQ Scores','Normalised PANAS Scores'])

#sns.set_style('whitegrid')
#ax= sns.stripplot(data=df)
#ax= sns.boxplot(data=df)
#plt.title('Spread of Affective State Scores')
#plt.show()


l = max(trial_length)
modes = []
for counter in range(l):
    values = []
    for i in options:
      if len(i)>counter: values.append(i[counter])
    modes.append(stats.mode(values).mode)
plt.plot([m+1 for m in modes])
plt.show()