import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

# Telegram bot configs
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = Bot(token=TOKEN)

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

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return  {
        'product_name': product_name,
        'old_price': int(old_price),
        'new_price': int(new_price),
        'installment_price': int(installment_price),
        'timestamp': timestamp
    }

def create_connection(db_name='iphone_prices.db'):
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn):
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS prices (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       product_name TEXT,
                       old_price INTEGER,
                       new_price INTEGER,
                       installment_price INTEGER,
                       timestamp TEXT
                   )
                   ''')
    conn.commit()

def save_to_database(conn, products_info):
    new_row = pd.DataFrame([products_info]) # convert the dict into a row DataFrame
    new_row.to_sql('prices', conn, if_exists='append', index=False) # save i the database

def get_max_price(conn):
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(new_price), timestamp FROM prices")
    result = cursor.fetchone()
    return result[0], result[1]
    
async def send_telegram_message(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)
    
async def main():
    
    # database configuration and setup
    conn = create_connection()
    setup_database(conn)
    
    df = pd.DataFrame()
    try:
        while True:
            # do the request and the page parsing
            page_content = fetch_page()
            products_info = parse_page(page_content)
            current_price = products_info["new_price"]
            
            # get max price 
            max_price, max_timestamp = get_max_price(conn)
            
            if current_price > max_price:
                print(f'Preço maior detectado: {current_price}')
                await send_telegram_message(f'Preço maior detectado: {current_price}')
                max_price = current_price # max price update
                max_timestamp = products_info['timestamp'] # max price timestamp update
            else:
                print(f'O maior preço registado é {max_price} em {max_timestamp}')
                await send_telegram_message(f'O maior preço registado é {max_price} em {max_timestamp}')

            # save the data in the database
            save_to_database(conn, products_info)
            print('DADOS SALVOS NO BANCO DE DADOS')
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        print("Parando a execução...")
    finally:
        # close database connection
        conn.close()

# exec asyncio loop   
asyncio.run(main())