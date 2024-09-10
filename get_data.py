from bs4 import BeautifulSoup
from selenium import webdriver

def scrape_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    target_class = "rogA2c"
    elements = soup.find_all(class_=target_class)
    
    print("\n")
    for element in elements:
        print(element.text)
    
    driver.quit()

def main():
    with open('places.txt', 'r') as file:
        urls = file.readlines()
    
    urls = [url.strip() for url in urls]
    
    for url in urls:
        scrape_page(url)

if __name__ == "__main__":
    main()

