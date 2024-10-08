import re
import json

def extract_info(text):
    # Split the input text by blank lines
    sections = [section.strip() for section in text.strip().split('\n\n')]
    
    data = []
    
    for section in sections:
        lines = section.split('\n')
        if len(lines) < 3:
            continue
        
        # Extract URL, place name, and address
        url = lines[0].strip()
        place_name = lines[1].strip()
        address = lines[2].strip()
        site = None
        contact_number = None
        
        # Search for site and contact number in the remaining lines
        remaining_lines = lines[3:]
        
        for line in remaining_lines:
            if '.com' in line:
                site_match = re.search(r'\b\w+\.com\b', line)
                site = site_match.group(0) if site_match else None

            if re.match(r'\b0\d+\b', line):
                contact_number = line.strip()
        
        data.append({
            'url': url,
            'place_name': place_name,
            'address': address,
            'site': site,
            'contact_number': contact_number
        })
    
    return data

# Read the content from the file
with open('details.txt', 'r') as file:
    content = file.read()

# Extract information
info = extract_info(content)

# Convert the extracted information to JSON and write to data.json
with open('data.json', 'w') as json_file:
    json.dump(info, json_file, indent=4)

print("Data has been written to data.json.")

