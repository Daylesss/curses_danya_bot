from aiogram import Router
from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.utils.bot_messages import bot_messages
from core.keyboards.inline import get_start_kb
from core.utils.fsm import BaseFSM
from core.keyboards import inline
from core.utils.database import db
from core.utils.fsm import Cmd_FSM
from core.handlers.course_handl import *

cmd_router = Router()

@cmd_router.message(Command("start"))
async def on_start(message: types.Message, state: FSMContext):
    await state.clear()
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
    await message.answer(bot_messages["start1"])
    await message.answer(bot_messages["start2"])
    await message.answer(bot_messages["start3"])
    await message.answer(bot_messages["start4"], reply_markup=get_start_kb())



@cmd_router.message(Command("new"))
async def next_theme(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(bot_messages["start4"], reply_markup=get_start_kb())

@cmd_router.message(Command("continue"))
async def next_theme(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Cmd_FSM.NEXT_THEME)
    await message.answer("Продолжить текущую тему?", reply_markup=inline.continue_theme_kb())


@cmd_router.callback_query(Cmd_FSM.NEXT_THEME, F.data=="not_continue")
async def not_continue_lesson(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 Нет")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")
    await state.clear()

@cmd_router.message(Command("next_theme"))
async def next_theme(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Cmd_FSM.NEXT_THEME)
    await message.answer(text="Вы действительно хотите начать следующую тему?", reply_markup=inline.next_theme_kb())

@cmd_router.callback_query(Cmd_FSM.NEXT_THEME, F.data=="Начать следующую")
async def to_next_theme(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if db.get_course_status(db.get_latest_course(db.get_user_id(callback.from_user.id))) == "end":
        await callback.message.answer("Данный курс кончился. Вы можете начать новый, пользуясь командой в меню.", reply_markup=inline.get_next_menu_kb())
        return
    day = db.get_day(callback.from_user.id) - 1
    if day < 20:
        db.update_day(db.get_latest_course(db.get_user_id(callback.from_user.id)), day+2)
        await callback.message.answer("Начинаем новый урок!")
        await start_course(callback=callback, state=state)
    else:
        await callback.message.answer("Это последняя тема в курсе. Вы можете начать новый курс или продолжить текущую тему.")

@cmd_router.callback_query(Cmd_FSM.NEXT_THEME, F.data=="Продолжить текущую")
async def continue_this(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if db.get_course_status(db.get_latest_course(db.get_user_id(callback.from_user.id))) == "end":
        await callback.message.answer("Данный курс кончился. Вы можете начать новый, пользуясь командой в меню.", reply_markup=inline.get_next_menu_kb())
        return
    day_status = db.get_day_status(callback.from_user.id)
    if day_status=="end":
        await callback.message.answer("Текущий урок уже закончился. Начинаем новый урок!")
        await start_course(callback=callback, state=state)
    else:
        await callback.message.answer("Продолжаем текущую тему.")
        if  day_status== "started" or day_status=="lecture":
            await start_course(callback=callback, state=state)
        elif day_status=="frameworks":
            await framework_answer(callback=callback, state=state)
        elif day_status == "advices":
            await advices_answer(callback=callback, state=state)
        elif day_status == "exercises":
            await exercises(callback=callback, state=state)
        else:
            await callback.answer("Что-то пошло не так.")
# @cmd_router.message(Command("menu"))
# async def menu(message: types.Message, state: FSMContext):
#     await state.clear()
#     await state.set_state(BaseFSM.MENU)
#     await message.answer("Здесь вы можете управлять своими курсами", reply_markup=inline.get_menu_kb())


@cmd_router.message(Command("about"))
async def about(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(BaseFSM.ABOUT)
    await message.answer(text="Здесь вы можете узнать об обучении", reply_markup=inline.get_about_kb())

@cmd_router.message(Command("support"))
async def support(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Ваши предложения, пожелания и вопросы вы можете написать в телеграмм @monoqle_support", reply_markup=inline.get_next_menu_kb())
