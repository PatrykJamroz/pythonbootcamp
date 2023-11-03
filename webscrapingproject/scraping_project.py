import requests
from bs4 import BeautifulSoup

quotes = []
is_fetching = True
base_url = 'https://quotes.toscrape.com/page/'
page_num = 1

while page_num < 2:
    r = requests.get(f"{base_url}{page_num}")
    html_string = r.text
    soup = BeautifulSoup(html_string, 'html.parser')
    found_quotes = soup.find_all(class_='quote')
    formatted_quotes = [{"quote": item.find(class_='text').get_text(), "author": item.find(class_='author').get_text(), "bio_url": item.find('a', string='(about)').get('href')} for item in found_quotes]
    quotes.extend(formatted_quotes)

    if soup.find(class_='next'):
        page_num += 1
    else: is_fetching = False



print(quotes)
print(len(quotes))