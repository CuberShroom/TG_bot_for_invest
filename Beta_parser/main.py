import asyncio
import logging
import sys
from os import getenv
from parser_run import Check_torf, quantity,price,secid, updatetime
from aiogram import Bot, html
from aiogram.client.default import DefaultBotProperties
from argparse import ArgumentParser
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import time
from aiogram.filters import CommandStart
from aiogram.types import Message



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
                print(Check_torf)
        
    if __name__ == "__main__":
        asyncio.run(main())


    
    