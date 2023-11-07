from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_command(bot: Bot):
    commands= [
        BotCommand(command= 'start', description= 'Начало работы'),
        BotCommand(command = 'menu', description= 'Главное меню')
        # BotCommand(command='sender', description='Создать рассылку')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())