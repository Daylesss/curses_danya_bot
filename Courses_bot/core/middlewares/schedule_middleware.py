from typing import Dict, Callable, Awaitable, Any
from apscheduler_di import ContextSchedulerDecorator
from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class ScheduleMiddleware(BaseMiddleware):
    def __init__(self, scheduler: ContextSchedulerDecorator) -> None:
        self.scheduler = scheduler
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["scheduler"] = self.scheduler
        
        return await handler(event, data)
        