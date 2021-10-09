import os
import json

def extract_json(filename):
    path = os.getcwd() + "/data/" + filename + ".json"
    with open(path) as jsonObj:
        data = json.load(jsonObj)
    
    return data
    
def convert_to_equiv_digits(equiv, num):
    return "".join([equiv[int(num)] for num in str(num)])