import sys
import json
import jsonschema
from jsonschema import validate
from jsonschema import Draft3Validator
import subprocess
from datetime import datetime


#zrobmy jakaś funkcje inicjującą, ktora dla danego pliku_test.py będzie sprawdzać czy zmiany nastąpiły
#dla plików, któymy _test jest zainteresowany. W szczególności puki co istotne są tylko pliki, które 
#są w folderze Model i mają rozszerzenie *.json

def check_existance(acr_file_json,value_to_check):
    splitted=value_to_check.split("_")

    msg=''
    for abb in splitted:
        exist_in_dict=False
        for item in acr_file_json['dictionary_items']:
            if item['short']==abb:
                exist_in_dict=True
        if exist_in_dict != True:
            msg+=abb + " "
    if len(msg)>0:
        return False,msg
    else:
        return True,msg

def check_acronyms(acronyms_file,json_data):
    with open(acronyms_file, "r") as file:
        acr_file_json = json.load(file)

    errors=''
    jsonTables=json_data['Table']

    for table in jsonTables:
        instance_exist, msg=check_existance(acr_file_json,table['@Name'])
        if  not instance_exist:
            errors+="Element Table @Na@Name "+ table['@Name'] + ": "+ msg+ " nie znajduje się w słowniku" + '\n'
        TableFields=table['Field']
        for tableField in TableFields:
            instance_exist, msg = check_existance(acr_file_json, tableField['@Name'])
            if not instance_exist:
                errors += "Element Field @Name "+ tableField['@Name'] + ": "+ msg+ "nie znajduje się w słowniku" + '\n'
            Mappings = tableField['Mapping']
            for mapping in Mappings:
                MappingSources = mapping['Source']
                for MappingSource in MappingSources:
                    MappingSourceFields = MappingSource['Filed']
                    for MappingSourceField in MappingSourceFields:
                        instance_exist, msg = check_existance(acr_file_json, MappingSourceField['@FileName'])
                        if not instance_exist:
                            errors += "Element Field @FileName " + MappingSourceField['@FileName'] \
                                      + ": " + msg  + " nie znajduje się w słowniku" + '\n'

    return errors

def log_data(file, dictionary_check_correct, err):
    dateLog = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    f = open(file.replace('.json','') + "_LOG.txt", "a")
    f.write(dateLog + " BUSINESS CHECKER - processing " + filepath + "\n")
    if(dictionary_check_correct):
        f.write("dictionary check OK")
    else:
        f.write(err)

    f.close()


def dictionary_test(files):

    dictionary_check_correct = True
    err = ''
    
    for file in files.split(" "):
        if (file.endswith('.json')):
            #err = check_acronyms("Dictionaries/table_name_acronyms.json",file)
            if (dictionary_check_correct == True and err != ''):
                dictionary_check_correct = False
            log_data(file, dictionary_check_correct, err)
    

def start_business_checker():
    files=subprocess.getoutput('git diff-tree --no-commit-id --name-only -r HEAD')
    dictionary_test(files)
