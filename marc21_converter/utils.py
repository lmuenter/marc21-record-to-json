import unicodedata


def read_xml_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        xml_string = file.read()
    return xml_string


def normalize_unicode(data):
    if isinstance(data, dict):
        return {k: normalize_unicode(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_unicode(item) for item in data]
    elif isinstance(data, str):
        return unicodedata.normalize('NFC', data)
    else:
        return data
    

def convert_to_digit(value):
    if value is not None and value.isdigit():
        return int(value)
    return value
