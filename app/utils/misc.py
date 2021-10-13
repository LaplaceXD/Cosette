import os
import json

def extract_json(filename):
    path = os.getcwd() + "/app/data/" + filename + ".json"
    with open(path) as jsonObj:
        data = json.load(jsonObj)
    
    return data
    
def convert_to_equiv_emoji_digits(num: int):
    digits = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    return "".join([digits[int(num)] for num in str(num)])