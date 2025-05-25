import os
import cv2
import pytesseract
import json
import re

# Folder containing the images and output file
image_folder = "./pictures"  # Replace with your folder path
output_file = "extracted_movie_data1.json"

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return ""
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img)
    return text

def parse_movie_data(text):
    movie_data = {}
    lines = text.split('\n')
    title_lines = []
    title_detected = False
    meta_info_processed = False
    bold_labels = ['Regie', 'Buch', 'Kamera', 'Montage', 'Musik', 'Ton', 'Produzentin', 'Produktion', 'Cast']
    type_mapping = {
        "spielfilm": "Spielfilm",
        "dokumentarfilm": "Dokumentarfilm",
        "mittellanger film": "Mittellanger Film",
        "kurzfilm": "Kurzfilm",
        "eröffnungsfilm": "Eröffnungsfilm",
        "kinderserie": "Kinderserie",
        "serie": "Serie" # Added "serie" to the mapping
    }
    current_section = None

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Capture consecutive uppercase lines as the title
        if not meta_info_processed and line.isupper():
            title_lines.append(line)
        elif title_lines and not meta_info_processed:
            # If we had uppercase lines, the next non-uppercase line signals the end of the title
            movie_data["title"] = " ".join(title_lines).strip()
            title_detected = True
            title_lines = [] # Reset
            # Now process the current line for meta info
            lower_line = line.lower()
            year_match = re.search(r'\b(\d{4})\b', lower_line)
            duration_match = re.search(r'(\d{1,3})\s*min\.', lower_line)
            origin_match = re.search(r'(deutschland|schweiz|österreich|albanien|irland)', lower_line)
            language_match = re.search(r'(mit\s*dt\.\s*ut|schweizermdt\.)', lower_line)
            type_found = False
            for key, value in type_mapping.items():
                if key in lower_line:
                    movie_data["type"] = value
                    type_found = True
                    break

            if year_match:
                movie_data["year"] = int(year_match.group(1))
            if duration_match:
                movie_data["duration"] = duration_match.group(1) + " Min."
            if origin_match:
                movie_data["origin"] = origin_match.group(0).capitalize()
            if language_match:
                movie_data["language"] = language_match.group(0)
            meta_info_processed = True
        elif not title_detected and line.isupper():
            movie_data["title"] = line
            title_detected = True
            # Process the next line for meta info immediately
            if i + 1 < len(lines):
                lower_next_line = lines[i + 1].strip().lower()
                year_match = re.search(r'\b(\d{4})\b', lower_next_line)
                duration_match = re.search(r'(\d{1,3})\s*min\.', lower_next_line)
                origin_match = re.search(r'(deutschland|schweiz|österreich|albanien|irland)', lower_next_line)
                language_match = re.search(r'(mit\s*dt\.\s*ut|schweizermdt\.)', lower_next_line)
                type_found = False
                for key, value in type_mapping.items():
                    if key in lower_next_line:
                        movie_data["type"] = value
                        type_found = True
                        break

                if year_match:
                    movie_data["year"] = int(year_match.group(1))
                if duration_match:
                    movie_data["duration"] = duration_match.group(1) + " Min."
                if origin_match:
                    movie_data["origin"] = origin_match.group(0).capitalize()
                if language_match:
                    movie_data["language"] = language_match.group(0)
                meta_info_processed = True

        # Standard extraction for other fields
        if any(word in line.lower() for word in ["synopsis", "eigentlich"]) and not any(b.lower() in line.lower() for b in bold_labels):
            movie_data["synopsis"] = line
            current_section = "synopsis"
        elif current_section == "synopsis" and not any(b.lower() in line.lower() for b in bold_labels):
            movie_data["synopsis"] += " " + line
        else:
            current_section = None

        if any(bold.lower() in line.lower() for bold in bold_labels):
            if "credits" not in movie_data:
                movie_data["credits"] = {}
            parts = line.split("|")
            for part in parts:
                for label in bold_labels:
                    if label.lower() in part.lower():
                        name = part.split(":")[-1].strip()
                        movie_data["credits"][label.lower()] = name

        # if any(day.lower() in line.lower() for day in ["mo", "di", "mi", "do", "fr", "sa", "so"]):
        #     movie_data.setdefault("screening_times", []).append(line.strip())

    # If title was spread across multiple uppercase lines
    if title_lines:
        movie_data["title"] = " ".join(title_lines).strip()

    return movie_data if movie_data.get("title") else {}

# Process all images in the folder
all_movie_data = []
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_folder, filename)
        print(f"Processing {filename}...")
        text = extract_text_from_image(image_path)
        movie_data = parse_movie_data(text)
        if movie_data:
            all_movie_data.append(movie_data)

# Save to JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_movie_data, f, ensure_ascii=False, indent=2)

print(f"✅ Data extracted and saved to {output_file}.")