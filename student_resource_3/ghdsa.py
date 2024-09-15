import re
import csv

# The entity-unit map (example subset based on Appendix)
entity_unit_map = {
  "width": {"centimetre", "foot", "millimetre", "metre", "inch", "yard"},
  "depth": {"centimetre", "foot", "millimetre", "metre", "inch", "yard"},
  "height": {"centimetre", "foot", "millimetre", "metre", "inch", "yard"},
  "item_weight": {"milligram", "kilogram", "microgram", "gram", "ounce", "ton", "pound"},
  "maximum_weight_recommendation": {"milligram", "kilogram", "microgram", "gram", "ounce", "ton", "pound"},
  "voltage": {"millivolt", "kilovolt", "volt"},
  "wattage": {"kilowatt", "watt"},
  "item_volume": {
      "cubic foot", "microlitre", "cup", "fluid ounce", "centilitre", "imperial gallon",
      "pint", "decilitre", "litre", "millilitre", "quart", "cubic inch", "gallon"
  }
}
possible_entity_unit_map = {
  "width": {"cm", "mm", "m", "ft", "in", "yd"},
  "depth": {"cm", "mm", "m", "ft", "in", "yd"},
  "height": {"cm", "mm", "m", "ft", "in", "yd"},
  "item_weight": {"mg", "kg", "μg", "g", "oz", "t", "lb", "lbs"},
  "maximum_weight_recommendation": {"mg", "kg", "μg", "g", "oz", "t", "lb", "lbs"},
  "voltage": {"mV", "kV", "V"},
  "wattage": {"kW", "W"},
  "item_volume": {"cu ft", "µL", "cup", "fl oz", "cL", "imp gal", "pt", "dL", "L", "mL", "qt", "cu in", "gal"}
}
unit_mapping = {
    "cm": "centimetre", "mm": "millimetre", "m": "metre", "ft": "foot", "in": "inch", "yd": "yard",
    "mg": "milligram", "kg": "kilogram", "μg": "microgram", "g": "gram", "oz": "ounce", "t": "ton", "lb": "pound", "lbs": "pound",
    "mV": "millivolt", "kV": "kilovolt", "V": "volt", 
    "kW": "kilowatt", "W": "watt", 
    "cu ft": "cubic foot", "µL": "microlitre", "cup": "cup", "fl oz": "fluid ounce", 
    "cL": "centilitre", "imp gal": "imperial gallon", "pt": "pint", 
    "dL": "decilitre", "L": "litre", "mL": "millilitre", "qt": "quart", 
    "cu in": "cubic inch", "gal": "gallon", "ml": "millilitre"
}
def extract_magnitude(text, entity_type):
    # Get the allowed units for the given entity type
    allowed_units = entity_unit_map.get(entity_type, set())
    possible_allowed_units = possible_entity_unit_map.get(entity_type, set())

    # Build a regex to match numbers followed by valid units
    units_pattern = '|'.join(re.escape(unit) for unit in allowed_units)
    possible_units_pattern = '|'.join(re.escape(unit) for unit in possible_allowed_units)
    pattern = r'(\d+\.?\d*)\s*(' + units_pattern + r')'
    possible_pattern = r'(\d+\.?\d*)\s*(' + possible_units_pattern + r')'

    # Search for matches in the text
    matches = re.findall(pattern, text, re.IGNORECASE)
    possible_matches = re.findall(possible_pattern, text, re.IGNORECASE)

    # Format the matches into the required "x unit" format
    extracted_magnitudes = [f"{num} {unit}" for num, unit in matches]
    possible_extracted_magnitudes = [f"{num} {unit}" for num, unit in possible_matches]
    
    if not extracted_magnitudes:
        extracted_magnitudes = ''
    if not possible_extracted_magnitudes:
        possible_extracted_magnitudes = ''
    return extracted_magnitudes, possible_extracted_magnitudes
# Read the CSV file and process the corresponding line in output.txt
csv_file = 'dataset/test.csv'  # Change this to the correct CSV file path
output_file = 'output/output.txt'
result_csv = 'output/result.csv'
possible_result_csv = 'output/possibleresult.csv'

# Open both files and prepare result CSV writers
with open(csv_file, 'r') as csvfile, open(output_file, 'r') as outputfile, \
        open(result_csv, 'w', newline='') as resultfile, open(possible_result_csv, 'w', newline='') as possibleresultfile:

    csv_reader = csv.reader(csvfile)
    output_lines = outputfile.readlines()  # Read all lines from output.txt

    result_writer = csv.writer(resultfile)
    possible_result_writer = csv.writer(possibleresultfile)

    # Write headers (optional)
    result_writer.writerow(['index', 'result'])
    possible_result_writer.writerow(['index', 'possible_result'])

    # Initialize counter
    i = 0

    # Iterate over both the CSV and output.txt
    for row, line in zip(csv_reader, output_lines):
        # Remove any extra whitespace from the line
        line = line.strip()

        # Extract the entity_type from the CSV (assuming it is the fourth column)
        image_id, image_url, number, entity_type = row

        # Call the extract_magnitude function with the current line and entity_type
        result, possible_result = extract_magnitude(line, entity_type)

        # Join the result lists into strings
        result_str = ', '.join(result) if result else ''
        possible_result_str = ', '.join(possible_result) if possible_result else ''
        if result:
            result_str = ','.join(result)
        elif possible_result:
            numa, unt = possible_result[0].split()
            full_unit = unit_mapping.get(unt, unt)
            
            if full_unit == possible_result[0]:
                result_str = ''
            else:
                result_str = f"{numa} {full_unit}"
        else:
            result_str = ''
        # Write results to result.csv and possibleresult.csv
        result_writer.writerow([i, result_str])
        possible_result_writer.writerow([i, possible_result_str])

        # Increment the counter
        i += 1

print("Processing completed. Results saved to result.csv and possibleresult.csv.")

