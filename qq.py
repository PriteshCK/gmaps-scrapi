from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def scrape_page(url):
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--force-device-scale-factor=0.1")  
    
    # Initialize WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Wait for new results to load

    # Scroll the sidebar to load all results
    scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")  # Sidebar div
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        time.sleep(5)  # Wait for new results to load
        
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        if new_height == last_height:
            break  # Stop scrolling if no new content loads
        last_height = new_height

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    target_class = "Nv2PK THOPZb CpccDe"  # Ensure this class is correct
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

def main():
    query = input("Search: ")
    search_url = "https://www.google.com/maps/search/" + query
    urls = scrape_page(search_url)

    with open('places.txt', 'w') as file:
        for url in urls:
            file.write(url + '\n')

if __name__ == "__main__":
    main()
