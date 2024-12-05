import argparse
import os
import glob
from generators.type_parser import parse_yaml
from generators.python_emitter import generate_python_types
from generators.ts_emitter import generate_ts_types

def process_file(input_file, output_dir):
    """
    Processes a single YAML file to generate Python and TypeScript files.
    """
    # Parse the YAML file
    types = parse_yaml(input_file)

    # Generate code
    python_code = generate_python_types(types)
    ts_code = generate_ts_types(types)

    # Generate output file names based on input file name
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    python_output_path = os.path.join(output_dir, f"{base_name}_types.py")
    ts_output_path = os.path.join(output_dir, f"{base_name}_types.ts")

    # Write Python code
    with open(python_output_path, "w") as py_file:
        py_file.write(python_code)

    # Write TypeScript code
    with open(ts_output_path, "w") as ts_file:
        ts_file.write(ts_code)

    print(f"Generated files for {input_file}:")
    print(f"  - Python: {python_output_path}")
    print(f"  - TypeScript: {ts_output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate Python and TypeScript types from YAML.")
    parser.add_argument("input", type=str, help="Path to the input YAML file or folder.")
    parser.add_argument("output", type=str, help="Output directory for generated files.")
    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Check if input is a single file or a folder
    if os.path.isfile(input_path):
        process_file(input_path, output_dir)
    elif os.path.isdir(input_path):
        # Process all YAML files in the folder
        yaml_files = glob.glob(os.path.join(input_path, "*.yaml"))
        if not yaml_files:
            print(f"No YAML files found in {input_path}.")
            return
        for yaml_file in yaml_files:
            process_file(yaml_file, output_dir)
    else:
        print(f"Invalid input path: {input_path}. Must be a file or a folder.")

if __name__ == "__main__":
    main()
