from aiogram import Bot
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv
from core.utils.database import db

load_dotenv(find_dotenv())

async def send_message_cron(bot: Bot):
    name_comp = 'send' + datetime.now().isoformat(timespec='hours')
    name_comp = name_comp.replace("-", "_")
    if not db.check_table(name_comp):
        db.create_sender_table(name_comp)
        
        # count = await senderlist.broadcaster(name_comp=name_comp, chat_id=chat_id, mesage_id=message_id, text_button=text_button, url_button=url_button)
            
        await bot.send_message(chat_id=int(os.getenv('ADMIN')), text='Рассылка прошла успешно.')
    db.delete_sender_table(name_comp)
    
    await bot.send_message(int(os.getenv('ADMIN')), text="Привет мир")