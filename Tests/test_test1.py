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
    

def validate_json(json_data):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema(json_data['SchemaName'])

    errCount = 0
    v = Draft3Validator(execute_api_schema)
    errors = v.iter_errors(json_data)

    logs_file = open("logs/errors.txt", "a")

    for error in sorted(errors, key=str):
        logs_file.write(error.message)
        errCount += 1
        
    if errCount > 0:
        err = "Given JSON data is InValid"
        logs_file.write(err)
        f.close()
        return False, err
    else:
        f.close()
        message = "Given JSON data is Valid"
        return True, message



def test_schema():
    is_wellformed=True
    msg=" Given JSON is well-formed"
    try:
        with open('Model/json_file.json', 'r') as file:
            json_file = json.load(file)
            is_valid, msg = validate_json(json_file)
            print(msg)
    except Exception as e:
        logs_file = open("logs/errors.txt", "a")
        logs_file.write(e)
        logs_file.write("JSON not  well-formed")
        logs_file.close()
        is_wellformed=False
        msg="JSON not  well-formed"
        
    print(msg)
    assert is_wellformed == True       

    assert is_valid == True 
