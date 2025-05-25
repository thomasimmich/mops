from pdf2image import convert_from_path
from PIL import Image
import os

# Define paths
pdf_path = "./temp/movies.pdf"  # Replace with your PDF file path
output_folder = "pictures"

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Convert PDF to images
images = convert_from_path(pdf_path)

# Process each image
for page_num, image in enumerate(images, start=1):
    # Get image dimensions
    width, height = image.size
    half_width = width // 2
    half_height = height // 2

    # Define coordinates for the four parts
    parts = [
        (0, 0, half_width, half_height),  # Top-left
        (half_width, 0, width, half_height),  # Top-right
        (0, half_height, half_width, height),  # Bottom-left
        (half_width, half_height, width, height)  # Bottom-right
    ]

    # Split and save each part
    for i, (left, top, right, bottom) in enumerate(parts, start=1):
        # Crop the image
        cropped_image = image.crop((left, top, right, bottom))
        
        # Save the cropped image
        output_path = os.path.join(output_folder, f"page_{page_num}_part_{i}.png")
        cropped_image.save(output_path, "PNG")
        print(f"Saved: {output_path}")

print("Processing complete!")