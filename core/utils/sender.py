import psycopg2
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramRetryAfter
# from asyncpg import Record
from typing import List
import asyncio
from aiogram.types import InlineKeyboardMarkup
from core.utils.database import MonoqleDB
from core.keyboards import inline


# class SenderList:
#     def __init__(self, bot: Bot, connector: asyncpg.pool.Pool) -> None:
#         self.bot=bot
#         self.connector= connector

#     async def get_keyboard(self, text_button: str, url_button: str):
#         keyboard_builder= InlineKeyboardBuilder()
#         keyboard_builder.button(text=text_button, url=url_button)
#         keyboard_builder.adjust(1)
#         return keyboard_builder.as_markup()

#     async def update_statuse(self, table_name, user_id, statuse, description):
#         async with self.connector.acquire() as connect:
#             query= f"UPDATE {table_name} SET statuse='{statuse}', description ='{description}' WHERE user_id={user_id}"
#             await connect.execute(query)

#     async def get_users(self, name_comp):
#         async with self.connector.acquire() as connect:
#             query=f"SELECT user_id FROM {name_comp} WHERE statuse='waiting'"
#             results_query: List[Record] = await connect.fetch(query)

#             return [result.get('user_id') for result in results_query]

#     async def send_message(self, user_id: int, from_chat_id: int, message_id: int, name_comp: str, keyboard: InlineKeyboardMarkup= None):
#         try:
#             await self.bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id, reply_markup=keyboard)
#         except TelegramRetryAfter as e:
#             await asyncio.sleep(e.retry_after)
#             return await self.send_message(self, user_id, from_chat_id, message_id, name_comp, keyboard)
#         except Exception as e:
#             await self.update_statuse(table_name=name_comp, user_id=user_id, statuse='Unsuccessful', description=f'{e}')
#         else: 
#             await self.update_statuse(table_name=name_comp, user_id=user_id, statuse='success', description='no errors')
#             return True
        
#         return False



#     async def broadcaster(self, name_comp: str, chat_id: int, mesage_id: int, text_button: str=None, url_button: str=None ):
#         keyboard= None
#         print(url_button, text_button)
#         if url_button:
#             keyboard= await self.get_keyboard(text_button=text_button, url_button=url_button)

#         users_ids = await self.get_users(name_comp=name_comp)
#         count = 0
#         try:
#             for user_id in users_ids:
#                 if await self.send_message(user_id=user_id, from_chat_id=chat_id, message_id=mesage_id, name_comp=name_comp, keyboard=keyboard):
#                     count+=1
#                 await asyncio.sleep(.05)
#         finally:
#             print(f'Сообщение отправлено {count}  пользовтелям')

#         return count
    
class Sender:
    def __init__(self, bot: Bot, db: MonoqleDB) -> None:
        self.bot=bot
        self.db = db
    
    async def new_lesson_reminder(self, user_id: int, name_comp: str):
        try:
            if self.db.get_course_status(self.db.get_latest_course(user_id)) == "paid":
                await self.bot.send_message(self.db.get_tg_id(user_id), text="Настало время для нового урока", reply_markup=inline.get_reminder_kb())
            else:
                self.db.update_statuse(table_name=name_comp, user_id=user_id, statuse='success', description='User did not buy the course')
                return False
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            return await self.new_lesson_reminder(self, user_id, name_comp)
        except Exception as e:
            self.db.update_statuse(table_name=name_comp, user_id=user_id, statuse='Unsuccessful', description=f'{e}')
        else: 
            self.db.update_statuse(table_name=name_comp, user_id=user_id, statuse='success', description='no errors')
            return True
        
        return False
    
    async def run_reminder(self, name_comp: str):

        users_ids = self.db.get_users(table_name=name_comp)
        count = 0
        try:
            for user_id in users_ids:
                if await self.new_lesson_reminder(user_id=user_id, name_comp=name_comp):
                    count+=1
                await asyncio.sleep(.05)
        finally:
            print(f'Сообщение отправлено {count}  пользователям')

        return count