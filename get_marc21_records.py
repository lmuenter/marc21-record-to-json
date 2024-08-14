import argparse
import json
from marc21_converter.parsers import parse_marc21_xml
from marc21_converter.utils import read_xml_file


def main():
    parser = argparse.ArgumentParser("This tool extracts record data from marc21 XML files.")
    parser.add_argument("-f", "--file", required=True, help="Path to xml file of marc21 standard")
    parser.add_argument("-o", "--output", required=True, help="Path to output file (json format)")

    args = parser.parse_args()

    xml_string = read_xml_file(args.file)

    parsed_data = parse_marc21_xml(xml_string)

    record_count = len(json.loads(parsed_data))

    with open(args.output, "w", encoding="utf-8") as json_file:
        json_file.write(parsed_data)

    print(f"[get_marc_21_records] Extracted {record_count} records from file: {args.file}. Saved in JSON-File: {args.output}")


if __name__ == "__main__":
    main()