import json
import re
import os
import numpy as np 

p = dict()
PANAS = dict()
PHQ = dict()
GAD = dict()
rewards = []
options = []
penalties = []

currentPenalty = 0

"""
creates a json of condensed data, removing prolific ids
"""


#CREATING A JSON THAT CONTAINS ANXIETY LEVELS AND LENGTH OF GAME
#ALSO CREATES ARRAY OF BOXES CHOSEN AND REWARDS

def check_consent(r):
    return not "No" in r

def store_age(r):
    substring = re.search(r'\"(.*)\"}', r).group(1)
    print(substring)
    p["age"]=substring

def store_gender(r):
    substring = re.search(r'\"(.*)\",\"Q1\"', r).group(1)
    print(substring)
    p["gender"]=substring

def strip_split(r):
    r = r.strip("{")
    r = r.strip("}")
    r = r.split(",")

    return r

def gender_age(r):
    r = r.split(":")
    store_age(r[2])
    store_gender(r[1])

def PANAS_item(r):
    r=r.split(":")
    PANAS[r[0]]=int(r[1])+1

def split_PANAS_line(r):
    r = strip_split(r)
    for each in r:
        PANAS_item(each)

def scorePANAS():
    PA = 0
    NA = 0
    PA_list=["Interested","Excited","Strong","Enthusiastic","Proud","Alert","Inspired","Determined","Attentive","Active"]
    NA_list=["Distressed","Upset","Guilty","Scared","Hostile","Irritable","Ashamed","Nervous","Jittery","Afraid"]
    for each in PANAS:
        word = each.strip(r'"')
        if(word in PA_list):
            PA+=PANAS[each]
        elif word in NA_list:
            NA+=PANAS[each]

    p['NA_score']=NA
    p['PA_score']=PA

def scorePHQ():
    total = 0
    for each in PHQ:
        total += PHQ[each]
    p['PHQ_score']=total

def scoreGAD():
    total = 0
    for each in GAD:
        total += GAD[each]
    p['GAD_score']=total


def store_item(r,index,p):
    r=r.split(":")
    if index ==p+1:
        PHQ[r[0]]=int(r[1])
    elif index==p+2:
        PHQ[r[0]+'b']=int(r[1])
    elif index==p+3:
        GAD[r[0]]=int(r[1])
    else:
        GAD[r[0]+'b'] =int(r[1])


def split_line(r,index,p):
    r = strip_split(r)
    for each in r:
        store_item(each,index,p)

def extract_arm(r):
    arm = r["button_pressed"]
    options.append(arm)

#def extract_rate(r):
   # rate = r["rate"]
    #rates.append(rate)

#def extract_prize(r):
   # if "#ff7157" in r["stimulus"]: prize = 0
   # if "#6dce98" in r["stimulus"]: prize = 1
   # rewards.append(prize)

def extract_reward(r):
    reward = r['reward']
    rewards.append(reward)

def extract_penalties(r):
    global currentPenalty
    fined = r['fined']
    if not fined: currentPenalty = 0
    penalties.append(currentPenalty)


def play(r):
    global currentPenalty
    if r['trial_type'] =="html-button-response": extract_arm(r)
    elif "reward" in r: extract_reward(r)
    elif "penalty" in r: currentPenalty = r['penalty']
    elif "fined" in r: extract_penalties(r)
        #extract_rate(r)
   # elif "stimulus" in r: #extract_prize(r)
    #scan each for each type then divert to its own individual function 

#To test just one file, uncomment line below
#filename = "IGT/data/igt_24-04-21-145858.json" 

def editName(n):
    n = n.strip("IGT/data/igt")
    n = "trial/clean" + n
    print(n)
    return n

def savefile():
    print("creating file")
    writefile = editName(filename)
    with open(writefile, "w") as f:
        json.dump(p,f)  

def resetParams():
    global rewards
    global options
    global penalties

    rewards.clear()
    options.clear()
    penalties.clear()


def scanLength(json_file):
     resetParams()
     data = json.load(json_file)
     PANAS_index = 100000
     for line in data:
        
        index = line['trial_index']
        #elif index==3:
        # print("prolific") #need to delete this

        if "responses" in line and ("Male" in line['responses'] or "Female" in line['responses']):
            gender_age(line['responses'])        
            
        if "responses" in line:
            if ("Interested" in line["responses"]) or ("Strong" in line["responses"]) or ("Enthusiastic" in line["responses"]) or ("Ashamed" in line["responses"]) or ("Attentive" in line["responses"]):
                split_PANAS_line(line['responses'])
                if ("Attentive" in line["responses"]):
                    p['PANAS']=PANAS
                    PANAS_index = index
                    scorePANAS()
      
        if index==PANAS_index+1 or index ==PANAS_index+2:
            split_line(line['responses'],index,PANAS_index)
            if index==PANAS_index + 2: 
                p['PHQ']=PHQ
                scorePHQ()

        if "responses" in line:        
            if index==PANAS_index+3 or index==PANAS_index+4:
                split_line(line['responses'],index,PANAS_index)
                if index==PANAS_index + 4:
                    p['GAD']=GAD
                    scoreGAD()
       # print(p)
        if line['trial_type']=="survey-text" and index>PANAS_index+15:
            print("end")
            p['length'] = index #saves how long the trial lasted
            p['options'] = options
            p['penalties'] = penalties
            p['rewards'] = rewards
           # savefile()
        elif PANAS_index +12 < index:
            #print("playing")
             play(line)
     #print("rewards: ",rewards)
    # print("penalties: ", penalties)
     print(np.sum(rewards)-np.sum(penalties))
     print("length: ", len(rewards), " ", len(penalties))
     print(f"\n")
    

directory ='igt/data'

#To create all data, uncomment line below
for filename in os.listdir(directory):
    print(os.path.join(directory, filename))
    if filename.endswith(".json"):
        json_file = open(os.path.join(directory, filename),'r')
        scanLength(json_file)

#for single file
#json_file = open(filename, 'r')        
#scanLength(json_file)
#print(p)
            

        