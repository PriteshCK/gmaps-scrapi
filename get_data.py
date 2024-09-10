from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_page(url):
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")  # Set a large window size to view more content
    chrome_options.add_argument("--force-device-scale-factor=0.1")  # Zoom to 50%

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # Allow some time for content to load fully
    driver.implicitly_wait(10)
    
    # Extract the page source and pass it to BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Define the class to look for
    target_class = "rogA2c"
    elements = soup.find_all(class_=target_class)
    
    # Print the results
    print("\n")
    for element in elements:
        print(element.text)
    
    driver.quit()

def main():
    # Read URLs from places.txt
    with open('places.txt', 'r') as file:
        urls = file.readlines()
    
    # Remove any extra whitespace or newline characters from the URLs
    urls = [url.strip() for url in urls]
    
    # Scrape each URL in the list
    for url in urls:
        scrape_page(url)

if __name__ == "__main__":
    main()

