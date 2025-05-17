import requests

def fetch_page(url):
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    url = 'https://www.mercadolivre.com.br/apple-iphone-16-pro-max-512-gb-titnio-natural-distribuidor-autorizado/p/MLB1040287864#polycard_client=search-nordic&searchVariation=MLB1040287864&wid=MLB3846015279&position=2&search_layout=stack&type=product&tracking_id=ddf60310-5b11-40b0-b4d3-d52723f2607f&sid=search'
    page_content = page_content(url)
    print(page_content)