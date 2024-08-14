import pytest
import json
import xml.etree.ElementTree as ET
from marc21_converter.parsers import parse_marc21_xml
from marc21_converter.utils import read_xml_file

def test_parse_marc21_xml():
    expected_keys = {"id", "format", "type", "title", "language"}
    expected_record_count = 2
    file_path = "assignment/daten.xml"

    xml_string = read_xml_file(file_path)
    result = json.loads(parse_marc21_xml(xml_string))
    print(result)

    for record in result:
        assert expected_keys.issubset(record.keys())
        assert(len(result) == expected_record_count)
