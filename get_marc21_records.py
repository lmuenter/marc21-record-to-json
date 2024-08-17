import argparse
import json
from marc21_converter.parsers import parse_marc21_xml, XMLValidationError
from marc21_converter.utils import read_xml_file
import os
import traceback


def main():
    parser = argparse.ArgumentParser("This tool extracts record data from marc21 XML files.")
    parser.add_argument("-f", "--file", required=True, help="Path to xml file of marc21 standard")
    parser.add_argument("-o", "--output", required=True, help="Path to output file (json format)")

    args = parser.parse_args()

    xsd_path = os.path.join(os.path.dirname(__file__), "marc21_converter", "schemas", "MARC21slim.xsd")
    
    # try parsing
    try:
        xml_string = read_xml_file(args.file)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' couldn't be found")
        return
    except IOError as e:
        print(f"Error: Encountered an I/O error while reading '{args.file}': {e}")
        return

    # try processing
    try:
        parsed_data = parse_marc21_xml(xml_string, xsd_path)
    except XMLValidationError as e:
        print(f"Error: XML validation failed. Details: {e}")
        return
    except ET.ParseError as e:
        print(f"Error: Failed to parse XML file. Details: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during parsing. Details: {e}")
        traceback.print_exc()
        return

    # try export
    try:
        record_count = len(json.loads(parsed_data))

        with open(args.output, "w", encoding="utf-8") as json_file:
            json_file.write(parsed_data)
    except IOError as e:
        print(f"Error: Encountered I/O Error while writing to file '{args.output}'")
    except Exception as e:
        print(f"An unexpected error occurred while writing to the output file. Details: {e}")
        traceback.print_exc()
        return

    # report
    print(f"[get_marc_21_records] Extracted {record_count} records from file: {args.file}. Saved in JSON-File: {args.output}")


if __name__ == "__main__":
    main()