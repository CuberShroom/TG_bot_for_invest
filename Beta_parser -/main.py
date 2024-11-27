import asyncio
import logging
import sys
from os import getenv
from parser_run import Check_torf, avg_quantity,avg_price,secid
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties


from aiogram.filters import CommandStart
from aiogram.types import Message
Check_torf
avg_quantity
avg_price
secid
bot= Bot(token='')
dp = Dispatcher()
Channel_link = '' 




@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
   

    await message.answer(f"Текст")


@dp.message()
async def echo_handler(message: Message) -> None:

    try:
        
        await message.send_copy(chat_id=Channel_link)

    except TypeError:
        
        await message.answer("Текст")
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    