from aiogram import Bot
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv
from core.utils.database import db
from core.utils.sender import Sender

load_dotenv(find_dotenv())

async def send_remainder(bot: Bot):
    name_comp = 'send' + datetime.now().isoformat(timespec='hours')
    name_comp = name_comp.replace("-", "_")

    sender = Sender(bot=bot, db=db)
    try:
        if not db.check_table(name_comp):
            db.create_sender_table(name_comp)
            
            count = await sender.run_reminder(name_comp=name_comp)
                
            await bot.send_message(chat_id=int(os.getenv('ADMIN')), text=f"Рассылка прошла успешно. Отправлено {count} сообщений.")
    except:
        await bot.send_message(int(os.getenv('ADMIN')), text="Во время ужедневной рассылки что-то пошло не так")
    finally:
        db.delete_sender_table(name_comp)