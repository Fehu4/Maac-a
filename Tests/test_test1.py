import sys
import json
import jsonschema
from jsonschema import validate
from jsonschema import Draft3Validator
import subprocess
from datetime import datetime
from io import StringIO
import test_business_test
import copy

def get_schema(schemaName):
    """This function loads the given schema available"""
    with open("Schema/" + schemaName, "r") as file:
        schema = json.load(file)
    return schema

def get_error_line(e, json_object):  
    marker = "3fb539deef7c4e2991f265c0a982f5ea"

    ob_tmp = copy.copy(json_object)
    for entry in list(e.path)[:-1]:
        ob_tmp = ob_tmp[entry]

    orig, ob_tmp[e.path[-1]] = ob_tmp[e.path[-1]], marker

    json_error = json.dumps(json_object, indent=4)
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
        #print("Line {} --- ".format(get_error_line(error, json_data)) + error.message)
        #error_text += "Line {}: ".format(get_error_line(error, json_data)) + error.message + "\n"
        error_text += ''.join([str(elem)+" " for elem in error.path]) + ": "
        error_text += error.message + "\n"
        errCount += 1
        
    if errCount > 0:
        message = "Given JSON data is InValid"
        return False, message, error_text
    else:
        message = "Given JSON data is Valid"
        return True, message, error_text


def create_documentation(file):
    print(file)
    doc_text = ''

    jsonObject = json.load(open(file))
    jsonSchema = json.load(open('Schema/'+jsonObject['SchemaName'],'r'))
    # with open(jsonObject['SchemaName'],'r') as schema_file:
    fields_in_doc = ['@Name','Project','Directive']

    for field in fields_in_doc:
        if (jsonObject['Table'][0][field] != ''):
            doc_text += '\n ' + field +' \t' + jsonObject['Table'][0][field]

    f = open(file.replace('.json','') + "_doc.html", "a")
    f.write(doc_text + "\n")
    f.close()

def extract_filename(filepath):
    splitted=filepath.split("/")

    return splitted[-1].replace('.json','')

def check_schema(filepath):
    is_wellformed = True
    is_valid = False

    dateLog = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    f = open(filepath.replace('.json','') + "_LOG.txt", "a")
    f.write(dateLog + " - processing " + filepath + "\n")
    f.write("TECHNICAL TESTS:\n")

    try:
        with open(filepath, 'r') as file:
            json_file = json.load(file)
            f.write("Given JSON data is well-formed\n")
            is_valid, msg, error_text = validate_json(json_file,f)
            print(msg)
            f.write(msg + "\n")
            if(is_valid == False):
                f.write(error_text + "\n")
    except Exception as e:
        print(e)
        is_wellformed=False
        msg="Given JSON data is not well-formed"
        print(msg)
        f.write(msg + "\n" + str(e) + "\n")

    f.close()

    create_documentation(filepath)

    if (is_wellformed and is_valid):
        return True
    else:
        return False


def test_main():
    # files=subprocess.getoutput('git diff-tree --no-commit-id --name-only -r HEAD')
    # for file in files.split(" "):
    #     if (file.endswith('.json')):
    #         technical_test_correct = check_schema(file)
    #         if (technical_test_correct):
    #             test_business_test.start_business_checker()

#             print(file)
   create_documentation('Projects/json_file.json')




