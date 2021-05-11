from lxml import etree

def inc(x):
    return x + 1

def validate(xml_path: str, xsd_path: str) -> bool:

    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_path)
    result = xmlschema.validate(xml_doc)

    return result


def test_schema():
    assert validate("json_file.json","json_schema.schema.json") == true 
