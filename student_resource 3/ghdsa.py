import re

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

def extract_magnitude(text, entity_type):
    # Get the allowed units for the given entity type
    allowed_units = entity_unit_map.get(entity_type, set())
    possible_allowed_units = possible_entity_unit_map.get(entity_type, set())

    extracted_magnitudes =[]
    possible_extracted_magnitudes =[]
    # Build a regex to match numbers followed by valid units
    units_pattern = '|'.join(re.escape(unit) for unit in allowed_units)
    possible_units_pattern = '|'.join(re.escape(unit) for unit in possible_allowed_units)
    pattern = r'(\d+\.?\d*)\s*(' + units_pattern + r')'
    possible_pattern = r'(\d+\.?\d*)\s*(' + possible_units_pattern + r')'

    
    # Search for matches in the text
    matches = re.findall(pattern, text, re.IGNORECASE)
    possible_matches = re.findall(possible_pattern, text, re.IGNORECASE)
    
    # Format the matches into the required "x unit" format
    extracted_magnitudes.append([f"{num} {unit}" for num, unit in matches])
    possible_extracted_magnitudes.append([f"{num} {unit}" for num, unit in possible_matches])
    
    # Return the first valid match, or an empty string if none are found
    if not extracted_magnitudes and not possible_extracted_magnitudes:
        return "",""
    elif extracted_magnitudes and not possible_extracted_magnitudes:
        return extracted_magnitudes,""
    elif not extracted_magnitudes and possible_extracted_magnitudes:
        return "",possible_extracted_magnitudes
    else:
        return extracted_magnitudes,possible_extracted_magnitudes

# Example usage:
text = "[([[np.int32(277), np.int32(65)], [np.int32(693), np.int32(65)], [np.int32(693), np.int32(133)], [np.int32(277), np.int32(133)]], 'DEMENSION', np.float64(0.9982118422778624)), ([[np.int32(360), np.int32(214)], [np.int32(550), np.int32(214)], [np.int32(550), np.int32(262)], [np.int32(360), np.int32(262)]], '3.76 inch', np.float64(0.8477059346237963)), ([[np.int32(734), np.int32(526)], [np.int32(782), np.int32(526)], [np.int32(782), np.int32(604)], [np.int32(734), np.int32(604)]], '5', np.float64(0.13658021309318347)), ([[np.int32(734), np.int32(604)], [np.int32(782), np.int32(604)], [np.int32(782), np.int32(704)], [np.int32(734), np.int32(704)]], '3', np.float64(0.9216260515146679))]"
entity_type = "width"

# Call the function
result,possible_result = extract_magnitude(text, entity_type)
print(result)  # Expected output: "25 kg"
print(possible_result)
