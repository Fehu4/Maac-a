import sys
import json
import jsonschema


def get_table_template_beggining():
    return '<table style="width:100%"><tr><th>Field name</th><th>Field value</th><th>Property name</th><th>Property value</th></tr>'

def get_table_template_ending():
    return '</table>'

def create_row(field_name,field_value,prop_name,prop_value):
    return '<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>'.format(field_name,field_value,prop_name,prop_value)

def loop_over(jsonObject, propertiesFields):

    doc_text = ''

    for fieldInJson in jsonObject:
        for fieldProperty in propertiesFields:
            
            value = jsonObject[fieldInJson]

            if (not isinstance(value, list)):

                return create_row(fieldInJson, value, fieldProperty, 'test')
            
            else:

                return (create_row(fieldInJson, 'ARRAY FOUND', fieldProperty, 'test') + loop_over(value, propertiesFields))



def create_documentation(file):

    jsonObject = json.load(open(file))

    jsonSchema = json.load(open('Schema/' + jsonObject['SchemaName'],'r'))

    jsonSchemaFragmentToSearchIn = jsonSchema['properties']['Table']['items']['properties']
    jsonObjectFragmentToSearchIn = jsonObject['Table'][0]

    fieldProps = ['description','type']

    doc_text = get_table_template_beggining()

    doc_text += loop_over(jsonObjectFragmentToSearchIn, fieldProps)

    doc_text += get_table_template_ending()

    f = open(file.replace('.json','') + "_doc.html", "w")
    f.write(doc_text)
    f.close()