import sys
import json
import jsonschema
from jsonschema import validate
from jsonschema import Draft3Validator
import subprocess
from datetime import datetime
from io import StringIO

def get_schema(schemaName):
    """This function loads the given schema available"""
    with open("Schema/" + schemaName, "r") as file:
        schema = json.load(file)
    return schema

# def get_json():
#     """This function loads json file"""
#     with open("json_file.json", "r") as file:
#         json_file = json.load(file)
#     return json_file

# def get_latest_files():
 
#     return files[]

def get_error_line(e, json_object):  
    marker = "3fb539deef7c4e2991f265c0a982f5ea"

    ob_tmp = json_object
    for entry in list(e.path)[:-1]:
        ob_tmp = ob_tmp[entry]

    orig, ob_tmp[e.path[-1]] = ob_tmp[e.path[-1]], marker

    json_error = json.dumps(json_object)
    io = StringIO(json_error)
    errline = None

    for lineno, text in enumerate(io):
            if marker in text:
                errline = lineno
                break
    return errline+1

def validate_json(json_data, f):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema(json_data['SchemaName'])
    
    errCount = 0
    v = Draft3Validator(execute_api_schema)
    errors = v.iter_errors(json_data)
    error_text=''
    for error in sorted(errors, key=str):
        print("Line {} --- ".format(get_error_line(error, json_data)) + error.message)
        error_text += error.message + "\n"
        errCount += 1
        
    if errCount > 0:
        message = "Given JSON data is InValid"
        return False, message, error_text
    else:
        message = "Given JSON data is Valid"
        return True, message, error_text


def create_documentation(file):
    body = """
            <html>
              <head>
                <meta name="pdfkit-page-size" content="Legal"/>
                <meta name="pdfkit-orientation" content="Landscape"/>
              </head>
                 Dokumentacja

                <body>""" + json.dumps(file, indent=4) + """</body>
            </html>
                """

    f = open("Model/Documentation/dokumentacja.html", "w")
    f.write(body + "\n")
    f.close()

def extract_filename(filepath):
    splitted=filepath.split("/")

    return splitted[-1].replace('.json','')

def check_existance(acr_file_json,value_to_check):
    splitted=value_to_check.split("_")

    msg=''
    for abb in splitted:
        if abb not in json.dumps(acr_file_json):
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
            errors+="Element Table @Na@Name"+ table['@Name'] + ": "+ msg+ " nie znajduje się w słowniku" + '\n'
        TableFields=table['Field']
        for tableField in TableFields:
            instance_exist, msg = check_existance(acr_file_json, tableField['@Name'])
            if not instance_exist:
                errors += "Element Field @Name"+ tableField['@Name'] + ": "+ msg+ "nie znajduje się w słowniku" + '\n'
            Mappings = tableField['Mapping']
            for mapping in Mappings:
                MappingSources = mapping['Source']
                for MappingSource in MappingSources:
                    MappingSourceFields = MappingSource['Filed']
                    for MappingSourceField in MappingSourceFields:
                        instance_exist, msg = check_existance(acr_file_json, MappingSourceField['@FileName'])
                        if not instance_exist
                            errors += "Element Field @FileName " + MappingSourceField['@FileName'] \
                                      + ": " + msg  + " nie znajduje się w słowniku" + '\n'

    return errors


def check_schema(filepath):
    is_wellformed = True
    is_valid = False

    dateLog = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    f = open("logs/"+extract_filename(filepath)+".txt", "a")
    f.write(dateLog + " processing " + filepath + "\n")

    try:
        with open(filepath, 'r') as file:
            json_file = json.load(file)
            is_valid, msg, error_text = validate_json(json_file,f)
            print(msg)
            f.write(msg + "\n" + error_text + "\n")
            create_documentation(json_file)
    except Exception as e:
        print(e)
        is_wellformed=False
        msg=filepath + " not  well-formed"
        print(msg)
        f.write(msg + "\n" + e + "\n")

    msg= check_acronyms("Dictionaries/table_name_acronyms.json",json_file)
    f.write(msg)
    f.close()
    assert is_wellformed == True       
    assert is_valid == True 


def test_test():
    files=subprocess.getoutput('git diff-tree --no-commit-id --name-only -r HEAD')
    for file in files.split(" "):
        if (file.endswith('.json')):
            check_schema(file)


