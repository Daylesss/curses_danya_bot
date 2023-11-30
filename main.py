import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Message, ContentType
import logging
from aiogram.filters import Command
from aiogram import F
from datetime import datetime, timedelta
from aiogram.utils.chat_action import ChatActionSender
from aiogram import Router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
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


#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    bot=Bot(token=os.getenv("BOT"), parse_mode='HTML')
    logging.basicConfig(level=logging.INFO)
    
    # jobstores = {
    #     "default": RedisJobStore(
    #         jobs_key="dispatched_trips_job",
    #         run_times_key="dispatched_trips_running",
    #         host = "localhost",
    #         db = 2,
    #         port = 6379
    #     )
    # }
    
    dp =Dispatcher()
    # scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone = "Europe/Moscow", jobstores=jobstores))
    # scheduler = AsyncIOScheduler(timezone = "Europe/Moscow")
    # scheduler.ctx.add_instance(bot, declared_class=Bot)
    # storage = RedisStorage.from_url("redis://localhost:6379/0")
    
    
    
    # scheduler.add_job(schedule.send_remainder, trigger='cron', start_date = datetime.now(), 
    #                 hour=10, minute = 0, kwargs= {"bot": bot})
    # scheduler.start()
    
    # dp.update.middleware(schedule_middleware.ScheduleMiddleware(scheduler))
    dp.include_routers(cmd_router, base_router, diag_router, course_router)
    
    await dp.start_polling(bot)


if __name__=='__main__':
    asyncio.run(main())