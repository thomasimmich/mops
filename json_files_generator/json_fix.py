import json
import os

def fix_concatenated_json_file(input_filepath, output_filepath=None):
    """
    Reads a JSON file containing concatenated JSON objects, wraps them in a JSON array,
    and optionally writes the result to a new JSON file.

    Args:
        input_filepath (str): Path to the input JSON file.
        output_filepath (str, optional): Path to the output JSON file.
                                         If None, the result is printed.
    """
    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            content = infile.read().strip()
            if not content:
                print(f"Warning: Input file '{input_filepath}' is empty.")
                return

            # Split the content into individual JSON-like objects
            objects = content.strip().split('}\n{')
            if len(objects) > 1:
                json_strings = []
                for i, obj_str in enumerate(objects):
                    obj_str = obj_str.strip()
                    if obj_str.startswith('{') and obj_str.endswith('}'):
                        json_strings.append(obj_str)
                    elif i == 0 and obj_str.endswith('}'):
                        json_strings.append(obj_str)
                    elif i == len(objects) - 1 and obj_str.startswith('{'):
                        json_strings.append(obj_str)
                    elif i > 0 and i < len(objects) - 1:
                        json_strings.append('{' + obj_str + '}')
                    elif i == 0:
                        json_strings.append(obj_str + '}')
                    elif i == len(objects) - 1:
                        json_strings.append('{' + obj_str)
                    else:
                        print(f"Warning: Could not parse segment: '{obj_str}' in '{input_filepath}'. Skipping.")
                        continue

                final_json_string = "[" + ",\n".join(json_strings) + "]"
            else:
                final_json_string = "[" + content.strip() + "]"

            if output_filepath:
                with open(output_filepath, 'w', encoding='utf-8') as outfile:
                    outfile.write(final_json_string)
                print(f"Processed '{input_filepath}' and saved to '{output_filepath}'.")
            else:
                print(f"Processed '{input_filepath}':")
                print(final_json_string)

    except FileNotFoundError:
        print(f"Error: Input file '{input_filepath}' not found.")
    except Exception as e:
        print(f"An error occurred while processing '{input_filepath}': {e}")

if __name__ == "__main__":
    json_files = [f for f in os.listdir('./temp') if f.endswith('.json')]
    for json_file in json_files:
        fix_concatenated_json_file(os.path.join('./temp', json_file), os.path.join('./temp', json_file)) # Overwrite the original file
        # If you want to create a new file, change the output_filepath:
        # output_file = json_file.replace('.json', '_fixed.json')
        # fix_concatenated_json_file(json_file, output_file)