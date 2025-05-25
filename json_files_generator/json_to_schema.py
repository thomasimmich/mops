import json
import re
import os

def transform_festival_data(raw_data, output_date=""):
    """
    Transforms the film schedule for a single day from a list of dictionaries.

    Args:
        raw_data (list): A list of dictionaries, where each dict represents
                         a cinema's schedule for the day.
        output_date (str, optional): The date of the schedule. If empty, it
                                     won't be explicitly set in the output.

    Returns:
        dict: The transformed JSON data for the day.
    """
    output_data = {}
    if output_date:
        output_data["date"] = output_date
    output_data["locations"] = []
    time_slots = ["10.00 Uhr", "12.00 Uhr", "14.00 Uhr", "16.00 Uhr", "19.00 Uhr", "21.00 Uhr"]

    for item in raw_data:
        location_name = item.get("KINO") or item.get("Unnamed: 0")
        if location_name:
            location_name = str(location_name).replace('\r', ' ').strip()
            screenings = []
            for time_slot in time_slots:
                screening_info = item.get(time_slot)
                if screening_info:
                    parts = screening_info.strip().split('\r')
                    start_time_with_program = parts[0]
                    match = re.match(r'(\d{2}:\d{2})\s*(.+)', start_time_with_program)
                    start_time = None
                    program_info = start_time_with_program.strip()

                    if match:
                        start_time = match.group(1)
                        program_info = match.group(2).strip()
                    elif re.match(r'\d{2}:\d{2}', start_time_with_program.split('\r')[0].strip().split(' ')[0]):
                        first_word = start_time_with_program.split(' ')[0].strip()
                        if re.match(r'\d{2}:\d{2}', first_word):
                            start_time = first_word
                            program_info = ' '.join(start_time_with_program.split(' ')[1:]).strip()

                    film_title = program_info
                    program_type = None
                    duration = None

                    film_parts = program_info.split('\n')
                    if len(film_parts) >= 2:
                        program_type = film_parts[0].strip()
                        film_title = film_parts[1].strip()
                    elif len(film_parts) == 1:
                        space_split = program_info.split(' ', 1)
                        if len(space_split) > 1 and space_split[0].isupper():
                            program_type = space_split[0].strip()
                            film_title = space_split[1].strip()
                        else:
                            film_title = space_split[0].strip()

                    duration_match = re.search(r'(\d+)\s+Min\.', ' '.join(parts))
                    if duration_match:
                        duration = f"{duration_match.group(1)} Min."

                    screenings.append({
                        "startTime": start_time,
                        "programType": program_type,
                        "filmTitle": film_title,
                        "duration": duration
                    })
                elif screening_info and isinstance(screening_info, str):
                    time_search = re.search(r'(\d{2}:\d{2})', screening_info)
                    extracted_start_time = None
                    remaining_title = screening_info.strip()
                    if time_search:
                        extracted_start_time = time_search.group(1)
                        remaining_title = screening_info.replace(extracted_start_time, '').strip('\r\n -')

                    screenings.append({
                        "startTime": extracted_start_time,
                        "programType": None,
                        "filmTitle": remaining_title,
                        "duration": None
                    })

            output_data["locations"].append({
                "locationName": location_name,
                "screenings": screenings
            })
    return output_data

if __name__ == "__main__":
    folder_path = "./final_json"  # Make sure this folder exists and contains your JSON files
    day_mapping = {
        "table_1.json": "DIENSTAG, 21.01.2025",
        "table_2.json": "DONNERSTAG, 23.01.2025",
        "table_3.json": "MITTWOCH, 22.01.2025",
        "table_4.json": "FREITAG, 24.01.2025",
        "table_5.json": "SAMSTAG, 25.01.2025",
        "table_6.json": "SONNTAG, 26.01.2025"
        # Add more mappings if you have more tables/files
    }

    final_output = {"schedule": []}

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
    else:
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                day = day_mapping.get(filename)
                if day:
                    print(f"Processing file: {filename} for {day}")
                    with open(file_path, 'r', encoding='utf-8') as file:
                        try:
                            data = json.load(file)
                            if isinstance(data, list):
                                transformed_data = transform_festival_data(data, output_date=day)
                                final_output["schedule"].append(transformed_data)
                            elif isinstance(data, dict):
                                transformed_data = transform_festival_data([data], output_date=day)
                                final_output["schedule"].append(transformed_data)
                            else:
                                print(f"Unexpected JSON structure in {file_path}. Expected a list or a dictionary.")

                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON from {file_path}: {e}")
                else:
                    print(f"No date mapping found for file: {filename}")

    print("\nFinal JSON Output:")
    final_json = json.dumps(final_output, indent=2, ensure_ascii=False)
    print(final_json)

    with open("final_festival_schedule.json", 'w', encoding='utf-8') as outfile:
        json.dump(final_output, outfile, indent=2, ensure_ascii=False)
    print("\nFinal transformed data saved to final_festival_schedule.json")