import log_likelihood as log_lklhd

class F_participant:
    def __init__(self,data):
        self.rewards = [int(x) for x in data['rewards']]
        self.options = [int(x) for x in data['options']]
        self.age = data['age']
        self.gender = data['gender']
        self.NA = data['NA_score']
        self.PA = data['PA_score']
        
