#!/bin/python3

"""
This script randomizes variable names in a PowerShell script using UUIDs.
Usage: python3 randomize_variables.py <path/to/powershell/script> [--prefix PREFIX] [--output OUTPUT_PATH]
"""

import re
import sys
import argparse
from uuid import uuid4

def get_file_content(path):
    """
    Read the content of the file at the given path.
    :param path: Path to the file to read.
    :return: Content of the file.
    """
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(1)

def generate_unique_variable(prefix, used_vars):
    """
    Generates a unique variable name with a minimum length of 20 characters.
    :param prefix: The prefix to be used for the variable name.
    :param used_vars: Set of already used variable names.
    :return: A unique variable name.
    """
    min_length = 40
    new_var_name = prefix
    while len(new_var_name) < min_length:
        new_var_name += uuid4().hex
    new_var_name = new_var_name[:min_length]
    
    if new_var_name in used_vars:
        return generate_unique_variable(prefix, used_vars)  # Recursive call to ensure uniqueness

    return new_var_name

def main():
    parser = argparse.ArgumentParser(description="Randomize variable names in a PowerShell script.")
    parser.add_argument("script_path", help="Path to the PowerShell script")
    parser.add_argument("--prefix", default="windowswindowswindowswindowswindows4444", help="Prefix for the variable names")
    parser.add_argument("--output", help="Output path for the modified script")
    args = parser.parse_args()

    payload = get_file_content(args.script_path)
    used_var_names = set()

    variable_definitions = re.findall(r'\$[a-zA-Z0-9_]+(?=\s*=)', payload)
    unique_vars = set(variable_definitions)

    for var in unique_vars:
        new_var_name = generate_unique_variable(args.prefix, used_var_names)
        used_var_names.add(new_var_name)
        payload = payload.replace(var, f'${new_var_name}')

    if args.output:
        with open(args.output, "w") as file:
            file.write(payload)
            print(f"Modified script written to {args.output}")
    else:
        print(payload)

if __name__ == "__main__":
    main()
