def read_xml_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        xml_string = file.read()
    return xml_string