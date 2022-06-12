import logging
import asyncio
from  aiogram import Bot, Dispatcher, executor, types

bot = Bot(token = "5380741935:AAHntlKxzbcntSYGM8zA4rPVtwTl0Gw2LZ4")


MY_ID = 736154341


async def upload():
    with open( '/home/catingblack/Рабочий стол/GF/img/7.jpg', 'rb') as file:
            file_id = 0
            msg = await bot.send_photo(MY_ID, file, disable_notification=True)
            file_id = msg.photo[-1].file_id
            print(f"file_id = {file_id}")


loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(upload()),
]

wait_tasks = asyncio.wait(tasks)
loop.run_until_complete(wait_tasks)
loop.close()


