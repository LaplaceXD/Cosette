import os
import json

def handle_indexes(index: int, Error: Exception, length: int = 0):
    if index < 0:
        index += length
    if index >= length or index < 0:
        raise Error("Index out of range!")

    return index

def extract_json(filename):
    path = os.getcwd() + "/app/data/" + filename + ".json"
    with open(path) as jsonObj:
        data = json.load(jsonObj)
    
    return data
    
def convert_to_equiv_digits(equiv, num):
    return "".join([equiv[int(num)] for num in str(num)])