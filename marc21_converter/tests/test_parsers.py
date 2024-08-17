import pytest
import json
import xml.etree.ElementTree as ET
from marc21_converter.parsers import parse_marc21_xml
from marc21_converter.utils import read_xml_file


def test_parse_marc21_xml():
    expected_keys = {"id", "format", "type", "title", "language", "publication_date", "contributors"}
    expected_record_count = 2
    file_path = "assignment/daten.xml"

    xml_string = read_xml_file(file_path)
    result = json.loads(parse_marc21_xml(xml_string))
    print(result)

    for record in result:
        assert expected_keys.issubset(record.keys())
        assert(len(result) == expected_record_count)


def test_publication_dates():
    """
    Asserts that array fields do not contain null in the output structure.
    
    Example: publication_date should return an Array. If null values are present, e.g. if no month, or day was given, only the year should be provided.
    """
    file_path = "assignment/daten.xml"
    xml_string = read_xml_file(file_path)
    results = json.loads(parse_marc21_xml(xml_string))
    for result in results:
        publication_date = result.get("publication_date", [])
        assert all(v is not None for v in publication_date), "Found None value in publication_date"
        assert all(v.isdigit() for v in publication_date), "Found non-numeric value in publication_date"

