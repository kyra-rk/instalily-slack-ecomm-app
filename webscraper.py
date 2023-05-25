from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# options for headless browser here
chrome_options = Options()

# Set headless mode
chrome_options.add_argument("--headless")

# get the target site
# https://scrapingclub.com/
# https://www.bedbathandbeyond.com/store/category/outdoor/patio-umbrellas-shades/gazebos-canopies/12463
# https://www.homedepot.com/b/Electrical-Fire-Safety-Fire-Extinguishers/N-5yc1vZbmgp
url = 'https://www.homedepot.com/b/Bath-Bathtubs-Alcove-Bathtubs/N-5yc1vZcd0g'
driver = webdriver.Chrome(
    options=chrome_options,
    service=Service(ChromeDriverManager().install())
)
driver.get(url)

# product scraping logic

products = []


class Product:
    def __init__(self, title, price, brand):
        self.title = title
        self.price = price
        self.brand = brand

    def __str__(self):
        return f"Name: {self.title}, Brand: {self.brand}, Price: {self.price}"

    def get_name(self):
        return self.title

    def get_price(self):
        return self.price

    def get_brand(self):
        return self.brand


def find_products(class_value):
    all_products = driver.find_elements(By.CLASS_NAME, "product-pod--s5vy1")
    for prod in all_products:
        html_source = prod.get_attribute("outerHTML")
        soup = BeautifulSoup(html_source, 'html.parser')
        price = find_price(soup)
        title = find_title(soup)
        brand = find_brand(soup)
        p = Product(title, price, brand)
        products.append(p)


def find_brand(soup):
    if soup is not None:
        x = soup.find(attrs={'class': 'product-header__title__brand--bold--4y7oa'})
        brand_str = x.text
        return brand_str


def find_title(soup):
    if soup is not None:
        x = soup.find(attrs={'class': 'product-header__title-product--4y7oa'})
        title_str = x.text
        # print(f'name: {title_str}')
        return title_str


def find_price(soup):
    if soup is not None:
        x = soup.find(attrs={'class': 'price-format__main-price'})
        price_str = x.text
        price_str = price_str[1:len(price_str):1]
        price_str = f'${int(price_str) / 100.0}'
        # print(price_str)
        # print(x.prettify())
        return price_str


def print_products():
    for p in products:
        print(p)


# find_element: Returns the first HTML element that matches the search condition.
# class="product-pod--s5vy1"
'''
prod = driver.find_element(By.CLASS_NAME, 'product-pod--s5vy1')
print(f'Product is of tag type: {prod.tag_name}')
print(f'Product inner html is: {prod.get_attribute("data-testid")}')
html_source = prod.get_attribute("outerHTML")
soup = BeautifulSoup(html_source, 'html.parser')
# print(soup.prettify())
'''
class_value_products = 'product-pod--s5vy1'
find_products(class_value_products)
print_products()

# release resources allocated by Selenium
# and shutdown the browser
driver.quit()
