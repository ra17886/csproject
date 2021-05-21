import json
import os
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


#use code in the pearson.py to compute correlations between individual phq and gad questions and compute heatmap
#PHQ QUESTIONS
"0: Little interest or pleasure in doing things"
"1: Feeling down, depressed, or hopeless"
"2: Trouble falling or staying asleep, or sleeping too much" 
"3: Feeling tired or having little energy"
"4: Poor appetite or overeating"
"5: Feeling bad about yourself - or that you are a failure or have let yourself or your family down"
"6: Trouble concentrating on things, such as reading the newspaper or watching television" 
"7: Moving or speaking so slowly that other people could have noticed? Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual"

#GAD QUESTIONS
"0: Feeling nervous, anxious or on edge"
"1: Not being able to stop or control worrying"
"2: Worrying too much about different things"
"3: Trouble relaxing"
"4: Being so restless that it is hard to sit still"
"5: Becoming easily annoyed or irritable"
"6: Feeling afraid as if something bad might happen"
       

directory = 'pvl_trial/'

PHQ = [[],[],[],[],[],[],[],[]]
GAD = [[],[],[],[],[],[],[]]

def getDetails(data):
    PHQdata = data['PHQ']
    GADdata = data['GAD']
    i = 0
    for item in PHQdata:
       # print(item, " ", PHQdata[item])
        PHQ[i].append(PHQdata[item])
       # print(i)
        i+=1
    j = 0
    for item in GADdata:
        GAD[j].append(GADdata[item])
        j+=1

for filename in os.listdir(directory):
    json_file = open(os.path.join(directory, filename),'r')
    data = json.load(json_file)
    getDetails(data)

df = pd.DataFrame(list(zip(PHQ[0],PHQ[1],PHQ[2],PHQ[3],PHQ[4],PHQ[5],PHQ[6],PHQ[7],GAD[0],GAD[1],GAD[2],GAD[3],GAD[4],GAD[5],GAD[6])),
               columns =['P1', 'P2','P3','P4', "P5", "P6", "P7","P8","G1","G2","G3","G4","G5","G6","G7"])
pearsoncorr = df.corr(method = 'pearson')
print(pearsoncorr)

for i in range(8):
    for j in range(7):
        corr,sig = pearsonr(PHQ[i],GAD[j])
        if sig <0.05 and corr>0.5:
         print("PHQ",i," vs GAD",j," Correlation:",corr," P-Value:","%.8f" %sig)



g = sb.heatmap(pearsoncorr, 
           xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.columns,
            cmap='coolwarm',
            annot=True,
            linewidth = 0.5,
            square = True
            )
plt.rcParams['figure.figsize']=(10,10)
plt.show()