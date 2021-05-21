import json 
import os

"""
Prints basic user stats, such as age ranges, genders and counts etc.
"""
age = []
gender =[]
gad =[]
phq = []
panasNA = []
panasPA = []
trial_length = []
likelihood = []
alpha = []
delta = []
phi = []
c = []

def getData(data):
    age.append(data['age'])
    gender.append(data['gender'])
    gad.append(int(data['GAD_score']))
    phq.append(int(data['PHQ_score']))
    panasNA.append(int(data['NA_score']))
    panasPA.append(int(data['PA_score']))
    trial_length.append(int(data['length']))
    likelihood.append(data['VSE_likelihood'])
    alpha.append(data['VSE_alpha'])
    delta.append(data['VSE_delta'])
    phi.append(data['VSE_phi'])
    c.append(data['VSE_c'])

directory = 'vse_trial'

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