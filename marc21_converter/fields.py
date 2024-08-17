import re
from marc21_converter._constants import IDENTIFIER_TAGS


def get_control_fields(record, namespace):
    controlfield_elements = record.findall(".//marc:controlfield", namespace)
    values = {}
    for controlfield_element in controlfield_elements:
        tag = controlfield_element.get("tag")
        if tag:
            values[tag] = controlfield_element.text
    return values

def get_medium_type(record, namespace, pos_start=5, ps_end=8):
    leader_element = record.find(".//marc:leader", namespace)
    if leader_element is not None:
        medium_type_code = leader_element.text[5:8]
        return medium_type_code
    return None

def get_data_field(record, namespace, tag, subfield_code):
    datafield_element = record.find(f".//marc:datafield[@tag='{tag}']", namespace)  # extract the specific tag
    if datafield_element is not None:
        subfield_element = datafield_element.find(f"marc:subfield[@code='{subfield_code}']", namespace)
        if subfield_element is not None:
            subfield_text = subfield_element.text
            return subfield_text
    return None
    
def get_full_title(record, namespace):
    title = get_data_field(record, namespace, tag="245", subfield_code="a") or ""
    subtitle = get_data_field(record, namespace, tag="245", subfield_code="b") or ""
    
    if title or subtitle:
        return f"{title if title else ''}{subtitle if subtitle else ''}"
    return None


def get_publication_date(record, namespace):
    parsed_data =  [
        get_data_field(record, namespace, "264", "c"), 
        get_data_field(record, namespace, "264", "d"), 
        get_data_field(record, namespace, "264", "e")
    ]

    if all(v is None for v in parsed_data[1:]):
         return list(filter(lambda item: item is not None, parsed_data))
    
    return parsed_data

def get_contributors(record, namespace):
    authors = get_authors(record, namespace, "100", "a", "4")
    institutes_first_authors = get_institutes(record, namespace, "110", "a", "4")
    further_authors = get_authors(record, namespace, "700", "a", "4")
    institutes_further_authors = get_institutes(record, namespace, "710", "a", "4")
    return authors + institutes_first_authors + further_authors + institutes_further_authors

def get_authors(record, namespace, tag, subfield_code, role_code):
    name_records = record.findall(f".//marc:datafield[@tag='{tag}']", namespace)

    authors = []

    for name_record in name_records:
        if name_record is not None:
            full_name = name_record.find(f"marc:subfield[@code='{subfield_code}']", namespace)
            role_name = name_record.find(f"marc:subfield[@code='{role_code}']", namespace)

            full_name_text = full_name.text
            name_parts_cleaned = [x.strip() for x in full_name_text.split(',')]

            author = {
                "given_name": name_parts_cleaned[1],
                "family_name": name_parts_cleaned[0],
                "role": role_name.text,
            }

            authors.append(author)

    return authors


def get_institutes(record, namespace, tag, subfield_code, role_code):
    name_records = record.findall(f".//marc:datafield[@tag='{tag}']", namespace)
    authors = []

    for name_record in name_records:
        if name_record is not None:
            name = name_record.find(f"marc:subfield[@code='{subfield_code}']", namespace)
            role = name_record.find(f"marc:subfield[@code='{role_code}']", namespace)

            author = {
                "name": name.text,
                "role": role.text,
                "corporation": True
            }

            authors.append(author)

    return authors


def get_identifiers(record, namespace):
    identifiers = []
    for identifier_type, tag_info in IDENTIFIER_TAGS.items():
        tag = tag_info["tag"]
        subfield_code = tag_info["subfield_code"]

        datafield = record.find(f".//marc:datafield[@tag='{tag}']", namespace)
        if datafield is not None:
            subfield = datafield.find(f".//marc:subfield[@code='{subfield_code}']", namespace)

            if subfield is not None:
                identifier = {
                    "type": identifier_type,
                    "value": subfield.text
                }
                identifiers.append(identifier)

    return identifiers
