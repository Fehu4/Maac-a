import sys
import json
import jsonschema
from jsonschema import validate
from jsonschema import Draft3Validator
import subprocess
from datetime import datetime
from io import StringIO
from BusinessChecker import start_business_checker

def get_schema(schemaName):
    """This function loads the given schema available"""
    with open("Schema/" + schemaName, "r") as file:
        schema = json.load(file)
    return schema

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

    doc_text = ''

    with open(file, 'r') as jsonObject:
        # with open(jsonObject['SchemaName'],'r') as schema_file:
        fields_in_doc = ['description', 'type']

        # for field in fields_in_doc:
        #     if (jsonObject[field] != ''):
        #         doc_text += '\n field \t' + jsonObject[field]

        body = """
                <html>
                <head>
                    <meta name="pdfkit-page-size" content="Legal"/>
                    <meta name="pdfkit-orientation" content="Landscape"/>
                </head>
                    Dokumentacja

                    <body>""" + doc_text + """</body>
                </html>
                    """

        ## DO ZMIANY - DOKUMENTACJA OBOK PLIKU KTÓRY BYŁ TESTOWANY
        f = open("Model/Documentation/dokumentacja.html", "w")
        f.write(body + "\n")
        f.close()

def extract_filename(filepath):
    splitted=filepath.split("/")

    return splitted[-1].replace('.json','')

def check_schema(filepath):
    is_wellformed = True
    is_valid = False

    dateLog = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    f = open(filepath.replace('.json','') + ".txt", "a")
    f.write(dateLog + " TECHNICAL TEST - processing " + filepath + "\n")

    try:
        with open(filepath, 'r') as file:
            json_file = json.load(file)
            is_valid, msg, error_text = validate_json(json_file,f)
            print(msg)
            f.write(msg + "\n" + error_text + "\n")
            #create_documentation(json_file)
    except Exception as e:
        print(e)
        is_wellformed=False
        msg=filepath + " not well-formed"
        print(msg)
        f.write(msg + "\n" + e + "\n")

    f.close()

    if (is_wellformed and is_valid):
        return True
    else:
        return False


def test_main():
    files=subprocess.getoutput('git diff-tree --no-commit-id --name-only -r HEAD')
    for file in files.split(" "):
        if (file.endswith('.json')):
            technical_test_correct = check_schema(file)
            if (technical_test_correct):
                start_business_checker()

            #print(file)
            #create_documentation(file)




