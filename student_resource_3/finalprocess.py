import csv
import os

# Define file path
csv_file = 'output/result.csv'  # Change this to your CSV file path

# Create a temporary file path
temp_csv_file = 'output/temp.csv'

try:
    # Read all rows into memory
    with open(csv_file, 'r', newline='') as infile:
        reader = list(csv.reader(infile))
    
    # Modify rows where necessary
    header = reader[0]  # Extract header
    rows = reader[1:]   # Extract rows
    
    for row in rows:
        # Check if the second column starts with a double-quote
        if row[1].startswith('\"'):
            # Replace with an empty string
            row[1] = ''
    
    # Write the modified rows to the temporary file
    with open(temp_csv_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write header
        writer.writerows(rows)   # Write modified rows

    # Replace the original file with the updated temporary file
    os.replace(temp_csv_file, csv_file)
    print("Processing completed. The original file has been updated.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure the temporary file is deleted
    if os.path.exists(temp_csv_file):
        os.remove(temp_csv_file)

