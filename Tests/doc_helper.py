import sys
import json
import jsonschema


def get_table_template_beggining():
    return '<table style="width:100%"><tr><th>Field name</th><th>Field value</th><th>Property name</th><th>Property value</th></tr>'

def get_table_template_ending():
    return '</table>'

def create_row(field_name,field_value,prop_name,prop_value):
    return '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(field_name,field_value,prop_name,prop_value)


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


def loop_over(jsonObject, jsonSchema, propertiesFields):
    doc_text = ''

    for fieldInJson in jsonObject:
        if (isinstance(fieldInJson, dict)):
            doc_text += loop_over(fieldInJson, jsonSchema, propertiesFields)
        else:
            value = jsonObject[fieldInJson]
            if (not isinstance(value,list)):

                for fieldProperty in propertiesFields:
                    doc_text += create_row(fieldInJson, value, fieldProperty,
                                   find_in_schema(jsonSchema, fieldInJson, fieldProperty,False))
            else:

                for fieldProperty in propertiesFields:
                    doc_text += create_row(fieldInJson, '', fieldProperty,
                                    find_in_schema(jsonSchema, fieldInJson, fieldProperty,False))
                doc_text += loop_over(value, jsonSchema, propertiesFields)

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