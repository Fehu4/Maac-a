import sys
import json
import jsonschema


def get_table_template_beggining():
    return '<table style="width:100%"><tr><th>Field name</th><th>Field value</th><th>Property name</th><th>Property value</th></tr>'

def get_table_template_ending():
    return '</table>'

def create_row(field_name,field_value,prop_name,prop_value):
    return '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(field_name,field_value,prop_name,prop_value)

def find_in_schema(jsonSchema, jsonField, props):

    for x in jsonSchema:
        if (x == jsonField):
            return jsonSchema[x][props]
        elif (isinstance(x, list)):
            find_in_schema(x,jsonField,props)


def loop_over(jsonObject, jsonSchema, propertiesFields):
    doc_text = ''

    for fieldInJson in jsonObject:
        for fieldProperty in propertiesFields:

            try:
                value = jsonObject[fieldInJson]
                doc_text += create_row(fieldInJson, value, fieldProperty,
                                       find_in_schema(jsonSchema, fieldInJson, fieldProperty))
            except TypeError:
                doc_text += (create_row(fieldInJson, '', fieldProperty,
                                        find_in_schema(jsonSchema, fieldInJson, fieldProperty))
                             + loop_over(value, jsonSchema, propertiesFields))

    return doc_text



def create_documentation(file):

    jsonObject = json.load(open(file))

    jsonSchema = json.load(open('Schema/' + jsonObject['SchemaName'],'r'))

    fieldProps = ['description','type']

    doc_text = get_table_template_beggining()

    doc_text += loop_over(jsonObject, jsonSchema, fieldProps)

    doc_text += get_table_template_ending()

    f = open(file.replace('.json','') + "_doc.html", "w")
    f.write(doc_text)
    f.close()