from aiogram import Router
from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.utils.bot_messages import bot_messages
from core.keyboards.inline import get_start_kb
from core.utils.fsm import BaseFSM
from core.keyboards import inline

cmd_router = Router()

@cmd_router.message(Command("start"))
async def on_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(bot_messages["start1"])
    await message.answer(bot_messages["start2"])
    await message.answer(bot_messages["start3"])
    await message.answer(bot_messages["start4"], reply_markup=get_start_kb())

@cmd_router.message(Command("menu"))
async def menu(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(BaseFSM.MENU)
    await message.answer("Здесь вы можете управлять своими курсами", reply_markup=inline.get_menu_kb())

