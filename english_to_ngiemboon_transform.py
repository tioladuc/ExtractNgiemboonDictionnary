from bs4 import BeautifulSoup
import requests
import csv
import re
import json
import os

from deep_translator import GoogleTranslator
Translator = GoogleTranslator(source='fr', target='en')


# ---- Dump (save) to UTF-8 text file ----
def save_file(data, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---- Later, load (recover) it back ----
def recover_file(file):
    recovered_data = []
    with open(file, "r", encoding="utf-8") as f:
        recovered_data = json.load(f)

    return recovered_data

# --- add elements in array and clean entries ----
def append(result, dialete, english):
    dialete = re.sub(r"\([^)]*\)", "", dialete)
    english = re.sub(r"\([^)]*\)", "", english)
    
    dialetes = dialete.split(';')
    englishs = english.split(';')
    
    for dial in dialetes:
        for engl in englishs:
            result.append({'ngiemboon':dial, 'en':engl})
    
    return result

# ---extract csv data ---
def extract_csv_data(data):
    temp_data = []
    for word in data:
        names = word['synonym']
        names.append(word['noun'])

        for definition in word['sensecontents']:
            for name in names:
                dialecte = definition["definition_en"]
                temp_data = append(temp_data, dialecte, name)

        for definition in word['sensecontents']:
            for example in definition['examples']:
                temp_data = append(temp_data, example['en'], example['dialect'])
    return temp_data


def save_data_as_csv(data, fieldnames, filename):    
    # Open the file in write mode ('w')    
    #print(filename)
    # return
    # The newline='' argument prevents extra blank rows in the CSV.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write all the data rows from the list of dictionaries
        writer.writerows(data)




directory = "english_to_ngiemboon_transform/"
directoryOld = "english_to_ngiemboon/"

data = {}
fileCompile = []
compteur = 0

files = os.listdir(directoryOld)
for file in files:
    print(file)
    file_data = recover_file(directoryOld + file)
    csv_data = extract_csv_data(file_data)
    fieldnames = ['en', 'ngiemboon']
    save_data_as_csv(csv_data, fieldnames, directory + file.replace(".txt", ".csv"))
    