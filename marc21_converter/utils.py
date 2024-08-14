import re


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


def read_xml_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        xml_string = file.read()
    return xml_string