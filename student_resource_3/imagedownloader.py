import csv
import requests
import os

# CSV file containing the data
csv_file = 'dataset/test.csv'
# Directory to save downloaded images
images_dir = 'images'

# Create the images directory if it doesn't exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

def is_valid_url(url):
    # Basic URL validation
    return url.startswith('http://') or url.startswith('https://')

# Read the CSV file and download images
with open(csv_file, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    for row in csv_reader:
        # Extract index and image URL from the CSV (assuming they are the first and second columns)
        index, image_url, _, _ = row
        
        # Check if URL is valid
        if not is_valid_url(image_url):
            print(f"Invalid URL skipped: {image_url}")
            continue
        
        # Set the image filename
        image_filename = f"{images_dir}/{index}.jpg"
        
        try:
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an error for bad responses
            
            # Save the image to the specified directory
            with open(image_filename, 'wb') as img_file:
                img_file.write(response.content)
            
            print(f"Downloaded {image_url} as {image_filename}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {image_url}: {e}")

print("All images have been downloaded.")

