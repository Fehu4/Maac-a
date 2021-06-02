import sys
import json
import jsonschema
from jsonschema import validate
from jsonschema import Draft3Validator
import subprocess
from datetime import datetime

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
    

def validate_json(json_data, f):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema(json_data['SchemaName'])
    
    errCount = 0
    v = Draft3Validator(execute_api_schema)
    errors = v.iter_errors(json_data)
    error_text=''
    for error in sorted(errors, key=str):
        print(error.path + " --- " + error.absolute_path + " --- " + error.message)
        error_text += error.path + " --- " + error.absolute_path + " --- " + error.message + "\n"
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

    f.close()
    assert is_wellformed == True       
    assert is_valid == True 


def test_test():
    files=subprocess.getoutput('git diff-tree --no-commit-id --name-only -r HEAD')
    for file in files.split(" "):
        if (file.endswith('.json')):
            check_schema(file)


