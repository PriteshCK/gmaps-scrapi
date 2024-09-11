from flask import Flask, request, jsonify
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--force-device-scale-factor=0.1")

# Initialize Flask app
app = Flask(__name__)

# query_places.py functionality
def scrape_places(query):
    driver = webdriver.Chrome(options=chrome_options)
    search_url = "https://www.google.com/maps/search/" + query + "+near+me"
    
    driver.get(search_url)
    driver.implicitly_wait(10)  # Wait for the page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    target_class = "Nv2PK THOPZb CpccDe"
    elements = soup.find_all(class_=target_class)
    
    urls = []
    for element in elements:
        a_tags = element.find_all('a', href=True)
        for a_tag in a_tags:
            href = a_tag['href']
            if "https://www.google.com/maps/place" in href:
                urls.append(href)
    
    driver.quit()
    return urls

def save_places_to_file(urls):
    with open('places.txt', 'w') as file:
        for url in urls:
            file.write(url + '\n')

# get_data.py functionality
def scrape_data_from_url(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(10)  # Wait for the page to load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    target_class = "rogA2c"
    elements = soup.find_all(class_=target_class)
    
    with open('details.txt', 'a') as file:
        file.write(f"{url}\n")
        
        tc = "DUwDvf lfPIob"
        node = soup.find(class_=tc)
        if node:
            file.write(node.text + '\n')
        
        for element in elements:
            text = element.text
            file.write(text + '\n')
        
        file.write('\n')
    
    driver.quit()

def scrape_all_places():
    with open('places.txt', 'r') as file:
        urls = [url.strip() for url in file.readlines()]
    
    for url in urls:
        scrape_data_from_url(url)

# jjson.py functionality
def extract_info_from_file():
    with open('details.txt', 'r') as file:
        content = file.read()
    
    sections = [section.strip() for section in content.strip().split('\n\n')]
    data = []
    
    for section in sections:
        lines = section.split('\n')
        if len(lines) < 3:
            continue
        
        url = lines[0].strip()
        place_name = lines[1].strip()
        address = lines[2].strip()
        site = None
        contact_number = None
        
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

@app.route('/scrape', methods=['POST'])
def scrape_api():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Step 1: Scrape places and save to places.txt
    urls = scrape_places(query)
    save_places_to_file(urls)
    
    if not urls:
        return jsonify({"message": "No URLs found"}), 404

    # Step 2: Scrape data from the URLs and save to details.txt
    open('details.txt', 'w').close()  # Clear the file before adding new content
    scrape_all_places()

    # Step 3: Extract the information and return as JSON
    extracted_data = extract_info_from_file()
    
    return jsonify({"data": extracted_data})

if __name__ == '__main__':
    app.run(debug=True)

