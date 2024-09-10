from bs4 import BeautifulSoup
from selenium import webdriver

def scrape_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
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
                print(href)
    
    driver.quit()
    return urls

def main():
    query = input("Search: ")
    search_url = "https://www.google.com/maps/search/" + query
    urls = scrape_page(search_url)
    
    with open('places.txt', 'a') as file:
        for url in urls:
            file.write(url + '\n')

if __name__ == "__main__":
    main()
