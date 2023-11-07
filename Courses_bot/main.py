import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message, ContentType
import logging
from aiogram.filters import Command
from aiogram import F
import asyncpg
from datetime import datetime, timedelta
from aiogram.utils.chat_action import ChatActionSender
from aiogram import Router
from core.handlers.base_nandl import base_router
from core.handlers.command_handl import cmd_router
from core.handlers.diagnostics import diag_router
from core.handlers.course_handl import course_router

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    bot=Bot(token="6547617401:AAHSU3c2O_S2G64OWJzdm4hs3h_W43K7_Y4", parse_mode='HTML')
    logging.basicConfig(level=logging.INFO)
    
    dp =Dispatcher()
    
    dp.include_routers(base_router, cmd_router, diag_router, course_router)
    
    await dp.start_polling(bot)


if __name__=='__main__':
    asyncio.run(main())