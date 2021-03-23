import json
import re

p = dict()
PANAS = dict()
PHQ = dict()
GAD = dict()

#when parsing strings, data starts after :\ and ends in \

def check_consent(r):
    return not "No" in r

def store_age(r):
    substring = re.search(r'\"(.*)\"}', r).group(1)
    p["age"]=substring

def store_gender(r):
    substring = re.search(r'\"(.*)\",\"Q1\"', r).group(1)
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
    
filename = 'mab_04-03-21-191536.json'


with open(filename) as json_file:
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
        
        
        elif index < 11 and index > 5:
            split_PANAS_line(line['responses'])
            if index ==10:
                p['PANAS']=PANAS
                scorePANAS()
            #maybe need to compute overall PANAS score?
            
        
        elif index==11 or index ==12:
            split_line(line['responses'],index)
            if index==12: 
                p['PHQ']=PHQ
                scorePHQ()
            #compute overall PHQ score

        
        elif index==13 or index==14:
            split_line(line['responses'],index)
            if index==14:
                p['GAD']=GAD
                scoreGAD()

        
        
        elif line['trial_type']=="survey-text" and index>22:
            p['length'] = index #saves how long the trial lasted
      #  elif index >22:
          #  print("playing")
           
    print(p)

        