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
    

def validate_json(json_data):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema(json_data['SchemaName'])
    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False, err
    message = "Given JSON data is Valid"
    return True, message



def test_schema(filepath):
    is_wellformed=True
    msg=" Given JSON is well-formed"
    try:
        with open(filepath, 'r') as file:
            json_file = json.load(file)
            is_valid, msg = validate_json(json_file)
            print(msg)
    except Exception as e:
        is_wellformed=False
        msg="JSON not  well-formed"
        
    print(msg)
    assert is_wellformed == True       

    assert is_valid == True 


test_schema(sys.argv[1])

