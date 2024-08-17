import xml.etree.ElementTree as ET
import json
from marc21_converter.fields import get_control_fields, get_medium_type, get_full_title, get_data_field, get_publication_date, get_contributors, get_identifiers, get_keywords
from marc21_converter.cleaners import clean_record
from marc21_converter._constants import DATA_MAPPING
from marc21_converter.utils import normalize_unicode
import xmlschema


class XMLValidationError(Exception):
    pass


def parse_marc21_xml(xml_string, xsd_path):
    validate_xml(xml_string, xsd_path)

    root = ET.fromstring(xml_string)
    namespace = {"marc": "http://www.loc.gov/MARC21/slim"}
    records = []
    for record in root.findall(".//marc:record", namespace):
        processed_record = process_record(record, namespace)
        cleaned_record = clean_record(processed_record, DATA_MAPPING)
        normalized_record = normalize_unicode(cleaned_record)
        records.append(normalized_record)
    return json.dumps(records, indent=2, ensure_ascii=False)


def process_record(record, namespace):
    controlfields = get_control_fields(record, namespace)

    processed_record = {
        "id": controlfields["001"],
        "format": controlfields["007"],
        "type": get_medium_type(record, namespace),
        "title": get_full_title(record, namespace),
        "language": get_data_field(record, namespace, tag="041", subfield_code="a"),
        "publication_date": get_publication_date(record, namespace),
        "contributors": get_contributors(record, namespace),
        "identifiers": get_identifiers(record, namespace),
        "keywords": get_keywords(record, namespace)
    }
    
    return processed_record


def validate_xml(xml_string, xsd_path):
    schema = xmlschema.XMLSchema(xsd_path)
    if not schema.is_valid(xml_string):
        raise XMLValidationError("XML validation against the schema failed.")

