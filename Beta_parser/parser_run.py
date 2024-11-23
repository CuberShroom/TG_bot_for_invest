import requests
import xml.etree.ElementTree as ET
import sqlite3
import threading
import time
from datetime import datetime, time as dtime
import asyncio
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, html
from aiogram.client.default import DefaultBotProperties
from argparse import ArgumentParser
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import time
from aiogram.filters import CommandStart
from aiogram.types import Message



# Данные для аутентификации
USERNAME = ''
PASSWORD = ''

# Интервалы работы парсера
START_TIME = dtime(8, 0)  # 8:00 UTC+3
END_TIME = dtime(21, 50)  # 21:50 UTC+3

# Функция для проверки времени работы парсера
def is_market_open():
    current_time = datetime.now().time()
    return START_TIME <= current_time <= END_TIME

# Получение списка SECID
def get_secid_list():
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        secid_list = []
        for data in root.findall(".//row[@SECID]"):
            secid = data.get('SECID')
            if secid:
                secid_list.append(secid)
        return secid_list
    else:
        print("Ошибка при получении списка SECID")
        return []
Check_torf=None
quantity=None
price= None
secid=None
updatetime=None
# Основная функция парсинга
def parse_data():

    global Check_torf, quantity,price,secid,updatetime

    secid_list = get_secid_list()
    
    while is_market_open():
        
        Check_torf = False
        for secid in secid_list:
            
            try:
                
                
                url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{secid}/orderbook.xml"
                response = requests.get(url, auth=(USERNAME, PASSWORD))
                if response.status_code == 200:
                    
                    root = ET.fromstring(response.content)
                    data_row = root.find(".//row")
                    if data_row is not None:
                        price = float(data_row.get('PRICE', '0'))
                        quantity = int(data_row.get('QUANTITY', '0'))
                        updatetime = data_row.get('UPDATETIME', '')
                        print(price,quantity,updatetime)
                        
                        db_name = f"Parser_Data_{secid}.db"
                        conn = sqlite3.connect(db_name)
                        c = conn.cursor()
                        c.execute('''CREATE TABLE IF NOT EXISTS data
                                     (price REAL, quantity INTEGER, updatetime TEXT)''')
                        c.execute("INSERT INTO data VALUES (?, ?, ?)", (price, quantity, updatetime))
                        conn.commit()

                        # Вычисление средних значений
                        c.execute("SELECT AVG(price) FROM data")
                        avg_price = c.fetchone()[0]
                        c.execute("SELECT AVG(quantity) FROM data")
                        avg_quantity = c.fetchone()[0]

                        # Проверка на аномальный рост
                        
                        if avg_price and price > avg_price * 2:
                            Check_torf = True
                            print(f"Main={Check_torf},{updatetime} {secid}MID_PRICE={avg_price}, {secid}MID_QUANTITY={avg_quantity}, {secid}, abnormal='Аномальный рост цены'")
                            
                             
                        elif avg_quantity and quantity > avg_quantity * 2:
                            Check_torf = True
                            print(f"Main={Check_torf},{updatetime} {secid}MID_PRICE={avg_price}, {secid}MID_QUANTITY={avg_quantity}, {secid}, abnormal='Аномальный рост объема'")
                            
                             
                        else:
                            print(f"Main={Check_torf} for {secid}")
                            Check_torf = False
                        
                        conn.close()
                           

                        
                        
                    else:
                        print(f"Нет данных для {secid}")
                    
                else:
                    print(f"Ошибка при получении данных для {secid}")
            except Exception as e:
                print(f"Ошибка при обработке {secid}: {e}")
              # Небольшая пауза между запросами
  
        time.sleep(1)  # Интервал 30 секунд между итерациями

    print("Торги завершены. Main=False")
while True:
    async def main():
        global Check_torf, quantity, price, secid, updatetime
        token = '7712132694:AAGqlice9PmZpI4SUzPq3m8ZVp_k7EWCs6Y'
        chat_id = '@TestChannelForinvestBot'
        message = f"""
            🟢 #{secid}
    ПОКУПКА  {price} руб.
    ОБЪЁМ {quantity}
    ВРЕМЯ {updatetime}
    ___________
            """


        
    
        async with Bot(
            token=token,
            default=DefaultBotProperties(
                
            ),
        ) as bot:
            if Check_torf== True:

                await bot.send_message(chat_id=chat_id, text=message)
                Check_torf=False
                print(Check_torf, secid)
                
            else:
                time.sleep(300)
                print(Check_torf)

                bot.send_message(chat_id='@trashFORMoex', text="Торги закрыты")
        
    if __name__ == "__main__":
        asyncio.run(main())
        threading.Thread(target=parse_data).start()
# Запуск парсера в отдельном потоке

