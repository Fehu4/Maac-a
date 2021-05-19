import json
import jsonschema
from jsonschema import validate


def get_schema():
    """This function loads the given schema available"""
    with open("json_schema.schema.json", "r") as file:
        schema = json.load(file)
    return schema

def get_json():
    """This function loads json file"""
    with open("json_file.json", "r") as file:
        json_file = json.load(file)
    return json_file
    

def validate_json(json_data):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema()

    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message


def test_if_wellFormed():
    is_valid=True
    msg=" Given JSON is well-formed"
    
    try:
        with open('json_file.json', 'r') as file:
            json_file = json.load(file)
    except ValueError as e:
        is_valid=False
        msg="JSON not  well-formed"
    
    print(msg)
    assert is_valid == True 

def test_schema():
    with open('json_file.json', 'r') as file:
        json_file = json.load(file)

    # validate it
    is_valid, msg = validate_json(json_file)
    print(msg)

    assert is_valid == True 
