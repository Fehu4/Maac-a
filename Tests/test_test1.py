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

    
    v = Draft3Validator(execute_api_schema)
    errors = v.iter_errors(json_data)
    for error in sorted(errors, key=str):
        print(error.message)
        
    if len(list(errors))>0:
        err = "Given JSON data is InValid"
        return False, err
    else:
        message = "Given JSON data is Valid"
        return True, message



def test_schema():
    is_wellformed=True
    msg=" Given JSON is well-formed"
    try:
        with open('Model/json_file.json', 'r') as file:
            json_file = json.load(file)
    except Exception as e:
        print(e)
        is_wellformed=False
        msg="JSON not  well-formed"
        
    print(msg)
    assert is_wellformed == True       
    
    # validate it
    is_valid, msg = validate_json(json_file)
    print(msg)

    assert is_valid == True 
