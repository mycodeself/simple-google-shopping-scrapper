import requests
import sys
import csv
import random 
from bs4 import BeautifulSoup
 
LIMIT = 50 # Valid values: 10, 20, 30, 40, 50, and 100

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
]
 
def make_request(searchTerm):
    assert isinstance(searchTerm, str), 'Search term must be a string'
    escaped_search_term = searchTerm.replace(' ', '+')
    limit = 50
    google_url = 'https://www.google.com/search?tbm=shop&q={}&num={}'.format(escaped_search_term, limit)
    response = requests.get(google_url, headers={'User-Agent': random.choice(USER_AGENTS)})
    response.raise_for_status() 
    print(response)
 
    return response.content

def parse_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    items = soup.find_all('div', attrs={'class': 'sh-dgr__grid-result'})
    for item in items:    
        price = item.find('span', attrs={'class': '_Fet'}).text
        seller = item.find('div', attrs={'class': '_NOs'}).find('div').text.replace(price, '')
        name = item.find('a', attrs={'class': '_oSs _NOs'}).text
        starsDiv = item.find('div', attrs={'class': '_OBj'})
        reviewsSpan = item.find('span', attrs={'class': '_Ezj'})
        reviews = 0
        if reviewsSpan:
            reviews = reviewsSpan.findNext('span').text
        stars = 0
        if starsDiv:
            stars = starsDiv['aria-label']
        results.append({'name': name, 'price': price, 'seller': seller, 'reviews': reviews,'stars': stars})
    print(results);
    return results;

def write_to_csv(filename, data):
    with open(filename + '.csv', 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())
        for item in data:
            writer.writerow(item.values())        

def parse_args():
    args = sys.argv
    length = len(args)
    if length < 2:
        print("No search term has been entered")
        sys.exit()
    if length > 2:
        print("I expect a single parameter dude")
        sys.exit()
    
    return args[1]

if __name__ == '__main__':
    searchTerm = parse_args()
    html = make_request(searchTerm)
    data = parse_content(html)
    if data:
        filename = searchTerm
        write_to_csv(filename, data)
    else:
        print("No data retrieve... maybe google ban :'( or try another search")
