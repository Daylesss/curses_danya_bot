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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from datetime import datetime
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from core.handlers.base_nandl import base_router
from core.handlers.command_handl import cmd_router
from core.handlers.diagnostics import diag_router
from core.handlers.course_handl import course_router
from core.utils.database import MonoqleDB
from core.utils import schedule
from core.middlewares import schedule_middleware
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#6443979698:AAGsrdgAHZfz0QmCHoReMFHj39-NiCyU7G0
async def main():
    bot=Bot(token=os.getenv("BOT"), parse_mode='HTML') # 6547617401:AAHSU3c2O_S2G64OWJzdm4hs3h_W43K7_Y4
    logging.basicConfig(level=logging.INFO)
    
    jobstores = {
        "default": RedisJobStore(
            jobs_key="dispatched_trips_job",
            run_times_key="dispatched_trips_running",
            host = "localhost",
            db = 2,
            port = 6379
        )
    }
    
    dp =Dispatcher()
    # scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone = "Europe/Moscow", jobstores=jobstores))
    # scheduler.ctx.add_instance(bot, declared_class=Bot)
    # storage = RedisStorage.from_url("redis://localhost:6379/0")
    
    
    
    # scheduler.add_job(schedule.send_message_cron, trigger='cron', start_date = datetime.now(), 
    #                   hour=datetime.now().hour, minute = datetime.now().minute + 1)
    # scheduler.start()
    
    # dp.update.middleware(schedule_middleware.ScheduleMiddleware(scheduler))
    dp.include_routers(base_router, cmd_router, diag_router, course_router)
    
    await dp.start_polling(bot)


if __name__=='__main__':
    asyncio.run(main())