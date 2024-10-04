"""
Brief: JUnit XML file processing script. Prepend classname to method name for each test case.
Author: Tomas Hladky
Date: 03.10.2024
"""

import xml.etree.ElementTree as ET
import argparse
import sys

# Error codes definition
EXIT_FAILURE_PARSE = 10
EXIT_FAILURE_FILE_NOT_FOUND = 11
EXIT_FAILURE_FILE_PERMISSIONS = 12
EXIT_FAILURE_ARG = 13
EXIT_FAILURE_CLASSNAME = 14
EXIT_FAILURE_NAME = 15
EXIT_FAILURE_OTHER = 100


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        usage="%(prog)s [options] [file]",
        description="JUnit XML file processing script. \
            Prepend classname to method name for each test case.",
    )
    parser.add_argument(
        "-j",
        required=False,
        action="store_true",
        dest="update",
        help="Update each test case in the file",
    )
    parser.add_argument(dest="file", nargs=1, help="File to process")
    args = parser.parse_args()

    if args.file is not None and not args.update:
        print("Missing -j option", file=sys.stderr)
        sys.exit(EXIT_FAILURE_ARG)

    process_file(args.file[0])


def process_file(filepath):
    """Process input XML file and output possibly updated content to stdout"""
    if filepath is None:
        print("Missing filepath", file=sys.stderr)
        sys.exit(EXIT_FAILURE_ARG)
    try:
        # Load XML file specified by argument
        tree = ET.parse(filepath)
        root = tree.getroot()

        for testcase in root.findall("testcase"):
            # Check if classname and name exist in testcase
            if "classname" not in testcase.attrib:
                print("Missing classname attribute", file=sys.stderr)
                sys.exit(EXIT_FAILURE_CLASSNAME)
            elif "name" not in testcase.attrib:
                print("Missing name attribute", file=sys.stderr)
                sys.exit(EXIT_FAILURE_NAME)

            # Prevent accumulated prepend
            splits = testcase.attrib["name"].rsplit(".", 1)
            if (
                len(splits) == 2 and testcase.attrib["classname"] == splits[0]
            ) or testcase.attrib["name"][:12] == "setUpClass (":
                continue

            # Prepend method name with classname
            testcase.attrib["name"] = (
                f"{testcase.attrib["classname"]}.{testcase.attrib["name"]}"
            )
    except ET.ParseError as e:
        print(f"Cannot parse XML file ${e}", file=sys.stderr)
        sys.exit(EXIT_FAILURE_PARSE)
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        sys.exit(EXIT_FAILURE_FILE_NOT_FOUND)
    except PermissionError as e:
        print(f"Access denied: {e}", file=sys.stderr)
        sys.exit(EXIT_FAILURE_FILE_PERMISSIONS)
    except RuntimeError as e:
        print(f"Unexpected error: ${e}", file=sys.stderr)
        sys.exit(EXIT_FAILURE_OTHER)
    else:
        # Parsing and modification finished successfully, out the new XML
        print(ET.tostring(root, encoding="unicode", xml_declaration=True))


if __name__ == "__main__":
    main()
