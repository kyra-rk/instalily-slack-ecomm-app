import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

print('start of scraper')

sitemap_links = []  # a list to store ALL links
category_links = {}  # a dictionary to store links for each category


def soup_info(s):
    print(f'soup.title:\n{s.title}\n')
    print(f'soup.title.name:\n{s.title.name}\n')
    print(f'soup.title.parent.name\n{s.title.parent.name}\n')
    print(f'soup.p\n{s.p}\n')

    print('soup.p[class]\n')
    print(s.p['class'])
    print('\n')

    print(f'soup.a\n{s.a}\n')

    print(f'soup.find_all\n')
    print(s.find_all('a'))
    print('\n')


def soup_links(soup):
    for link in soup.find_all('a'):
        url = link.get('href')
        sitemap_links.append(url)


''' Takes the sitemap links, finds their categories and adds them to a dictionary under their categories.
'''


def get_categories():
    for link in sitemap_links:
        # urlparse() function takes a link and returns a named tuple representing components of a URL
        parsed_url = urlparse(link)
        # the 'path' attribute of the parsed URL contains the path component of the URL as a string
        # we can use the split() method to extract individual components
        path_components = parsed_url.path.split('/')
        # usually a product link will have at least 3 components and the second component is the word 'category' itself
        # eg. /store/category/baby-kids/car-seats/infant-car-seats/12971
        if len(path_components) >= 3 and path_components[2] == 'category':
            category = path_components[3]
        else:
            category = 'uncategorized'

        # append link to the right category in the dictionary
        if category in category_links:
            category_links[category].append(link)
        else:
            category_links[category] = [link]


def print_category_names():
    print('\nAll categories: \n')
    for category in category_links:
        print(category)
    print('\n')


def print_category_links():
    for category, links in category_links.items():
        print(f"Category: {category}")
        for link in links:
            print(f" - {link}")


def print_all_links():
    for link in sitemap_links:
        print(link)
    print('\n')


class Product:
    def __init__(self, name, company, price):
        self.name = name
        self.company = company
        self.price = price


def get_product_card(link):
    # request for product
    rp = requests.get(link, timeout=10)
    if r.status_code == 200:
        # soup for product
        sp = BeautifulSoup(rp.content, 'html.parser')
        print('PRETTIFIED \n\n')
        print(sp.prettify())
        print('GENERAL a tags\n\n')
        for a in sp.find_all('a'):
            print(a.prettify())
        print('PRODUCT CARDS \n\n')
        for prod in sp.find_all('div', class_="prodCardR"):
            print(prod.prettify())
        print("SOUP: \n\n")
        print(sp)
    else:
        print(f'error with product card link: {link}\n\n')


try:

    # Making a GET request
    # home depot: https://www.homedepot.com/c/site_map
    # bed bath and beyond: 'https://www.bedbathandbeyond.com/sitemap'
    r = requests.get('https://www.bedbathandbeyond.com/sitemap', timeout=60)

    # check status code for response received
    # success code is 200
    if r.status_code == 200:
        # step 1: print content of request
        print(f'Successfully requested {r.url}')
        # print(r.content)

        # step 2: make the soup
        soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup.prettify())

        # step 3: access info about the soup
        # soup_info(soup)

        # only extract the URLs found within the page's <a> tags
        soup_links(soup)
        print_all_links()
        get_categories()
        print_category_names()
        print("CATEGORY LINKS: \n")
        print_category_links()
        # testing
        # get_product_card('https://www.bedbathandbeyond.com/store/category/outdoor/patio-umbrellas-shades/gazebos-canopies/12463')
    else:
        print(f'Request failed with the status code: {r.status_code}')

except requests.exceptions.Timeout:
    print('The request timed out at 60 seconds.')

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')
