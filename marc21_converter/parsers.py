import xml.etree.ElementTree as ET
import json
from marc21_converter.utils import get_control_fields, get_medium_type, get_full_title


mapping = {
    "format": {
        "tu": "print",
        "cr": "electronic",
    },
    "type": {
        "cam": "book",
        "caa": "article",
    }
}


def parse_marc21_xml(xml_string):
    root = ET.fromstring(xml_string)
    namespace = {"marc": "http://www.loc.gov/MARC21/slim"}
    records = []
    for record in root.findall(".//marc:record", namespace):
        processed_record = process_record(record, namespace)
        cleaned_record = clean_record(processed_record, mapping)
        records.append(cleaned_record)
    return json.dumps(records, indent=2)

def process_record(record, namespace):
    controlfields = get_control_fields(record, namespace)

    processed_record = {
        "id": controlfields["001"],
        "format": controlfields["007"],
        "type": get_medium_type(record, namespace),
        "title": get_full_title(record, namespace),
    }
    
    return processed_record


def clean_record(processed_record, mappings):
    cleaned_record = {}
    for key, value in processed_record.items():
        if key in mappings:
            cleaned_value = mappings[key].get(value, value)
            cleaned_record[key] = cleaned_value
        else:
            cleaned_record[key] = value
    return cleaned_record
