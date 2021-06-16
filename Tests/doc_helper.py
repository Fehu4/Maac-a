import sys
import json
import jsonschema

MAIN_FIELDS = ["@NAME", "PROJECT"]
FIELD_PROPS = ['description','type','maxLength','pattern']


def get_table_template_beggining():
    return '<table style="width:100%"><tr><th style="width: 20%">Field name</th><th style="width: 40%">Field value</th><th>Property name</th><th>Property value</th></tr>'

def get_table_template_ending():
    return '</table>'

def create_row(field_name, field_value, prop_name, prop_value, is_next, indents_number):

    indents_to_add = ''

    for i in range(0, indents_number):
        indents_to_add += ' - - '

    if (field_name in MAIN_FIELDS):
        return '<tr>' \
           '<td><strong style="font-size: 30px">{0}</strong></td>' \
           '<td><strong style="font-size: 30px">{1}</strong></td>'.format(field_name, field_value)
    elif (is_next and prop_value == None):
        return ''
    elif (is_next):
        return '<tr>' \
           '<td>{0}</td>' \
           '<td>{1}</td>' \
           '<td style="border: 1px solid black">{2}</td>' \
           '<td style="border: 1px solid black">{3}</td></tr>'.format('', '', prop_name,
                                                                              prop_value)
    else:
        return '<tr>' \
           '<td style="border: 1px solid black">{0}</td>' \
           '<td style="border: 1px solid black">{1}</td>' \
           '<td style="border: 1px solid black">{2}</td>' \
           '<td style="border: 1px solid black">{3}</td></tr>'.format(indents_to_add + field_name, field_value, prop_name,
                                                                              prop_value)

def find_in_schema(jsonSchema, jsonField, props, found):
    for x in jsonSchema:
        if (found and x == props):
            return jsonSchema[x]
        elif (x == jsonField and isinstance(jsonSchema[x],dict)):
            return find_in_schema(jsonSchema[x],jsonField,props,True)
        elif (isinstance(jsonSchema[x],dict)):
            result =  find_in_schema(jsonSchema[x], jsonField, props, False)
            if (result != None):
                return result
            else:
                continue


def loop_over(jsonObject, jsonSchema, propertiesFields, indents_number):

    doc_text = ''

    for fieldInJson in jsonObject:
        if (fieldInJson in MAIN_FIELDS):
            doc_text += create_row(fieldInJson, jsonObject[fieldInJson], '', '', False, indents_number + 1)
        elif (isinstance(fieldInJson, dict)):
            doc_text += loop_over(fieldInJson, jsonSchema, propertiesFields, indents_number + 1)
        else:
            value = jsonObject[fieldInJson]
            if (not isinstance(value,list)):

                for fieldProperty in propertiesFields:
                    doc_text += create_row(fieldInJson, value, fieldProperty,
                                   find_in_schema(jsonSchema, fieldInJson, fieldProperty,False),propertiesFields.index(fieldProperty), indents_number + 1)
            else:

                for fieldProperty in propertiesFields:
                    doc_text += create_row(fieldInJson, '', fieldProperty,
                                    find_in_schema(jsonSchema, fieldInJson, fieldProperty,False),propertiesFields.index(fieldProperty), indents_number + 1)
                doc_text += loop_over(value, jsonSchema, propertiesFields, indents_number + 1)

    return doc_text



def create_documentation(file):

    jsonObject = json.load(open(file))

    jsonSchema = json.load(open('Schema/' + jsonObject['SchemaName'],'r'))

    doc_text = get_table_template_beggining()

    doc_text += loop_over(jsonObject, jsonSchema, FIELD_PROPS, -3)

    doc_text += get_table_template_ending()

    f = open(file.replace('.json','') + "_doc.html", "w")
    f.write(doc_text)
    f.close()