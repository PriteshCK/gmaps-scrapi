from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_page(url):
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Required for running as root
    chrome_options.add_argument("--force-device-scale-factor=0.1")  # Set zoom to 50%

    # Initialize WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for the page to load fully
    driver.implicitly_wait(10)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find elements by the target class
    target_class = "Nv2PK THOPZb CpccDe"
    elements = soup.find_all(class_=target_class)
    
    urls = []
    for element in elements:
        a_tags = element.find_all('a', href=True)
        for a_tag in a_tags:
            href = a_tag['href']
            if "https://www.google.com/maps/place" in href:
                urls.append(href)
                print(href)
    
    # Quit the driver
    driver.quit()
    return urls

def main():
    query = input("Search: ")
    search_url = "https://www.google.com/maps/search/" + query
    urls = scrape_page(search_url)
    
    # Write URLs to places.txt
    with open('places.txt', 'a') as file:
        for url in urls:
            file.write(url + '\n')

if __name__ == "__main__":
    main()

