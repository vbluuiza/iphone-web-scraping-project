import requests
from bs4 import BeautifulSoup
import time

def fetch_page():
    url = 'https://www.mercadolivre.com.br/apple-iphone-16-pro-max-512-gb-titnio-natural-distribuidor-autorizado/p/MLB1040287864#polycard_client=search-nordic&searchVariation=MLB1040287864&wid=MLB3846015279&position=2&search_layout=stack&type=product&tracking_id=ddf60310-5b11-40b0-b4d3-d52723f2607f&sid=search'
    response = requests.get(url)
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('h1', class_= 'ui-pdp-title').get_text()
    prices:list = soup.find_all('span', class_='andes-money-amount__fraction')
    old_price = prices[0].get_text().replace('.', '')
    new_price = prices[1].get_text().replace('.', '')
    installment_price = prices[2].get_text().replace('.', '')

    return  {
        'product_name': product_name,
        'old_price': old_price,
        'new_price': new_price,
        'installment_price': installment_price
    }

if __name__ == '__main__':
    while True:
        page_content = fetch_page()
        products_info = parse_page(page_content)
        print(products_info)
        time.sleep(10)