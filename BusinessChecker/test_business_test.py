import sys
import json
import jsonschema
from jsonschema import validate
from jsonschema import Draft3Validator
import subprocess


#zrobmy jakaś funkcje inicjującą, ktora dla danego pliku_test.py będzie sprawdzać czy zmiany nastąpiły
#dla plików, któymy _test jest zainteresowany. W szczególności puki co istotne są tylko pliki, które 
#są w folderze Model i mają rozszerzenie *.json
def test_business_test_1():
    assert True == True
