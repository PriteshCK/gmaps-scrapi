from flask import Flask, request, jsonify, Response
import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--force-device-scale-factor=0.1")


chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=3840,2160")

# initialize Flask app
app = Flask(__name__)

# query_places.py functionality
def scrape_places(query):
    driver = webdriver.Chrome(options=chrome_options)
    search_url = "https://www.google.com/maps/search/" + query
    
    driver.get(search_url)
    driver.implicitly_wait(10)  # Wait for the page to load


    # scroll sidebar
#    scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
#    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
#    
#    while True:
#        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
#        time.sleep(5)
#        
#        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
#        if new_height == last_height:
#            break
#        last_height = new_height


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
    
    print(len(urls))
    driver.quit()
    return urls

def save_places_to_file(urls):
    with open('places.txt', 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\n')

# get_data.py functionality
def scrape_data_from_url(url):
    print(url)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(10)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    target_class = "rogA2c"
    elements = soup.find_all(class_=target_class)
    
    with open('details.txt', 'a', encoding='utf-8') as file:
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
    with open('places.txt', 'r', encoding='utf-8') as file:
        urls = [url.strip() for url in file.readlines()]
    
    for url in urls:
        scrape_data_from_url(url)

# jjson.py functionality
def extract_info_from_file():
    with open('details.txt', 'r', encoding='utf-8') as file:
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
    
    # clear,write extracted data to data.json
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    
    return data

@app.route('/scrape', methods=['POST', 'GET'])
def scrape_api():
    if request.method == 'POST':
        query = request.json.get('query')
    else:
        query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # scrape places, save to places.txt
    urls = scrape_places(query)
    save_places_to_file(urls)
    
    if not urls:
        return jsonify({"message": "No URLs found"}), 404

    # scrape data from the URLs and save to details.txt
    open('details.txt', 'w', encoding='utf-8').close()  # Clear the file before adding new content
    scrape_all_places()

    # extract info, save to data.json, and return content
    extracted_data = extract_info_from_file()
    
    # Read contents of data.json
    with open('data.json', 'r', encoding='utf-8') as json_file:
        json_output = json.load(json_file)

    # Return JSON without sorting
    return Response(json.dumps(json_output, indent=4, sort_keys=False, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    #app.run(debug=True, host='192.168.0.106', port=5000)
    app.run(debug=True, host='0.0.0.0', port=5000)
