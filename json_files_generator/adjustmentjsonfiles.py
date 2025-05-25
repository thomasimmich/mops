import json
import re
import os

def restructure_kino_data(data):
    restructured_data = []
    if not isinstance(data, list) or not data:
        return restructured_data

    time_slots = ["10.00 Uhr", "12.00 Uhr", "14.00 Uhr", "16.00 Uhr", "19.00 Uhr", "21.00 Uhr"]

    for item in data:
        kino_name = None
        output_item = {"KINO": None}
        for slot in time_slots:
            output_item[slot] = None

        first_key = list(item.keys())[0] if item else None
        first_value = list(item.values())[0] if item else None

        if first_key and first_value and "KINO" in first_key:
            lines = first_value.strip().split('\r')
            kino_match = re.search(r"^(CineStar|Filmhaus|Kino|camera zwo|Passage|Kinowerkstatt)(.*)", lines[0])
            if kino_match:
                kino_name = kino_match.group(1).strip() + (f" {kino_match.group(2).strip()}" if kino_match.group(2).strip() else "")
                output_item["KINO"] = kino_name

                for key, value in item.items():
                    if key.startswith("Unnamed"):
                        time_index = int(key.split(":")[1]) if ":" in key else None
                        if time_index is not None and 0 <= time_index < len(time_slots) and value:
                            output_item[time_slots[time_index]] = value.strip().replace('\r', ' ')
                if output_item["KINO"]:
                    restructured_data.append(output_item)
            elif len(lines) > 0:
                # Try to get the kino name from the start of the first line
                potential_kino = lines[0].split()[0]
                if potential_kino in ["CineStar", "Filmhaus", "Kino", "camera", "Passage", "Kinowerkstatt"]:
                    output_item["KINO"] = lines[0].strip()
                    for key, value in item.items():
                        if key.startswith("Unnamed"):
                            time_index = int(key.split(":")[1]) if ":" in key else None
                            if time_index is not None and 0 <= time_index < len(time_slots) and value:
                                output_item[time_slots[time_index]] = value.strip().replace('\r', ' ')
                    if output_item["KINO"]:
                        restructured_data.append(output_item)
        elif first_key and first_key.startswith("SAMSTAG"):
            value = item[first_key]
            lines = value.strip().split('\r')
            if len(lines) > 2:
                kino_match = re.search(r"^(CineStar|Filmhaus|Kino|camera zwo|Passage|Kinowerkstatt)(.*)", lines[2])
                if kino_match:
                    kino_name = kino_match.group(1).strip() + (f" {kino_match.group(2).strip()}" if kino_match.group(2).strip() else "")
                    output_item["KINO"] = kino_name
                    for key, current_value in item.items():
                        if key.startswith("Unnamed"):
                            time_index = int(key.split(":")[1]) if ":" in key else None
                            if time_index is not None and 0 <= time_index < len(time_slots) and current_value:
                                output_item[time_slots[time_index]] = current_value.strip().replace('\r', ' ')
                    if output_item["KINO"]:
                        restructured_data.append(output_item)

    # Clean up entries where only "KINO" is present
    final_restructured = [item for item in restructured_data if any(item.get(slot) for slot in time_slots) or item.get("KINO")]
    return final_restructured

def fix_and_restructure_json_file(input_filepath, output_filepath=None):
    """
    Reads a JSON file, restructures the data, and optionally writes to a new JSON file.
    """
    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            content = infile.read().strip()
            if not content:
                print(f"Warning: Input file '{input_filepath}' is empty.")
                return

            try:
                data = json.loads(content)
                if isinstance(data, list):
                    restructured = restructure_kino_data(data)
                    if output_filepath:
                        with open(output_filepath, 'w', encoding='utf-8') as outfile:
                            json.dump(restructured, outfile, indent=2, ensure_ascii=False)
                        print(f"Processed '{input_filepath}' and saved to '{output_filepath}'.")
                    else:
                        print(json.dumps(restructured, indent=2, ensure_ascii=False))
                else:
                    print(f"Warning: Expected a JSON list in '{input_filepath}'.")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in '{input_filepath}': {e}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_filepath}' not found.")
    except Exception as e:
        print(f"An error occurred while processing '{input_filepath}': {e}")

if __name__ == "__main__":
    input_folder = './temp/test'
    output_folder = './game'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
    for json_file in json_files:
        input_path = os.path.join(input_folder, json_file)
        output_path = os.path.join(output_folder, f"{os.path.splitext(json_file)[0]}_fixed.json")
        fix_and_restructure_json_file(input_path, output_path)

    print(f"\nProcessed all JSON files in '{input_folder}' and saved the restructured versions to '{output_folder}'.")