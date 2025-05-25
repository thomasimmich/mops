## Data Extraction and Pre-processing Pipeline

This project outlines a series of Python scripts used to extract and pre-process data from PDF documents related to a schedule and movies.

### Steps:

1.  **Table Extraction (`Table_extracter.py`)**
    * Extracts tables containing schedule information from the `tables.pdf` file.

2.  **PDF to Images (`pdftoimg.py`)**
    * Converts a PDF containing movie information into a series of images, splitting the data into 4 pages.

3.  **Data Extraction from Images (`Extractdatapics.py`)**
    * Extracts data about movies from the generated images and outputs it in JSON format.

4.  **JSON Data Fixing (`json_fix.py`)**
    * Performs pre-processing to fix data issues specifically found in tables 5 and 6 of the extracted data.

5.  **JSON File Adjustments (`adjustmentjsonfiles.py`)**
    * Makes minor adjustments at the end of the generated JSON files to resolve any inconsistencies.

6.  **JSON to Schema Conversion (`json_to_schema.py`)**
    * Converts the processed JSON files into JSON schema, defining the structure of the data.

### Usage:

To run the pipeline, execute the Python scripts in the order listed above. Ensure that the necessary input files (`tables.pdf` and the movie information PDF) are present in the correct locations.

```
python Table_extracter.py
python pdftoimg.py
python Extractdatapics.py
python json_fix.py
python adjustmentjsonfiles.py
python json_to_schema.py```
