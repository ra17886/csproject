import json
import re
import os

p = dict()
PANAS = dict()
PHQ = dict()
GAD = dict()
rewards = []
options = []
rates = []


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


def store_item(r,index):
    r=r.split(":")
    if index ==11:
        PHQ[r[0]]=int(r[1])
    elif index==12:
        PHQ[r[0]+'b']=int(r[1])
    elif index==13:
        GAD[r[0]]=int(r[1])
    else:
        GAD[r[0]+'b'] =int(r[1])


def split_line(r,index):
    r = strip_split(r)
    for each in r:
        store_item(each,index)

def extract_arm(r):
    arm = r["button_pressed"]
    options.append(arm)

def extract_rate(r):
    rate = r["rate"]
    rates.append(rate)

def extract_prize(r):
    if "#ff7157" in r["stimulus"]: prize = 0
    if "#6dce98" in r["stimulus"]: prize = 1
    rewards.append(prize)

def play(r):
    if r['trial_type'] =="html-button-response": extract_arm(r)
    elif "rate" in r: extract_rate(r)
    elif "stimulus" in r: extract_prize(r)
    #scan each for each type then divert to its own individual function 

#To test just one file, uncomment line below
#filename = "mab/data/mab_05-03-21-154538.json" 

def editName(n):
    n = n.strip("mab/data/mab")
    n = "options_trial/clean" + n
    print(n)
    return n

def savefile():
    print("creating file")
    writefile = editName(filename)
    with open(writefile, "x") as f:
        json.dump(p,f)  

def resetParams():
    global rewards
    global options
    global rates

    rewards.clear()
    options.clear()
    rates.clear()


def scanLength(json_file):
     resetParams()
     data = json.load(json_file)
     for line in data:
        index = line['trial_index']

        if index == 1 or index== 2:
            consent = check_consent(line['responses'])
            if not consent:
                print("Consent form void")
                break
           
        #elif index==3:
        # print("prolific") #need to delete this

        elif index==4:
            gender_age(line['responses'])        
            
        elif index < 11 and index > 6:
            split_PANAS_line(line['responses'])
            if index ==10:
                p['PANAS']=PANAS
                scorePANAS()
                
                
            
        elif index==11 or index ==12:
            split_line(line['responses'],index)
            if index==12: 
                p['PHQ']=PHQ
                scorePHQ()
                

            
        elif index==13 or index==14:
            split_line(line['responses'],index)
            if index==14:
                p['GAD']=GAD
                scoreGAD()
            
        elif line['trial_type']=="survey-text" and index>22:
            p['length'] = index #saves how long the trial lasted
            p['options'] = options
            p['rates'] = rates
            p['rewards'] = rewards
            savefile()
        elif index >22:
              play(line)
    

directory ='mab/data'

#To create all data, uncomment line below
for filename in os.listdir(directory):
    print(os.path.join(directory, filename))
    if filename.endswith(".json"):
        json_file = open(os.path.join(directory, filename),'r')
        scanLength(json_file)

#json_file = open(filename, 'r')        
#scanLength(json_file)
#print(p)
            

        