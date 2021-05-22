import sys
import json
import jsonschema
from jsonschema import validate
from jsonschema import Draft3Validator

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
    for error in sorted(errors, key=str):
        print(error.message)
        f.write(error.message+ "\n")
        errCount += 1
        
    if errCount > 0:
        err = "Given JSON data is InValid"
        return False, err
    else:
        message = "Given JSON data is Valid"
        return True, message


def test_schema(filepath):
    is_wellformed=True


    f = open("errors.txt", "a")
    f.write("Processing " + filepath + "\n")


    try:
        with open(filepath, 'r') as file:
            json_file = json.load(file)
            is_valid, msg = validate_json(json_file,f)
            print(msg)
            f.write(msg + "\n")
    except Exception as e:
        print(e)
        is_wellformed=False
        msg=filepath + " not  well-formed"
        print(msg)
        f.write(msg + "\n")

    assert is_wellformed == True       

    assert is_valid == True 
    f.close()

test_schema(sys.argv[1])

