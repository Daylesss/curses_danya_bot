from aiogram import Router
from aiogram import Bot, Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
import json
from core.utils.fsm import DiagFSM, CourseFSM
from core.keyboards import inline
from core.utils.chatgpt import get_course_plan
from core.utils.database import db
diag_router = Router(name="diag")

@diag_router.callback_query(F.data == "К диагностике")
async def position(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await state.set_state(DiagFSM.POSITION)
    try:
        await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    except:
        print("Не удалось изменить сообщение")
    await callback.message.answer(text="Контент для какой компетенции Вам интересен?")
    await callback.message.answer(text="Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_position_kb())



@diag_router.callback_query(DiagFSM.POSITION)
async def model_of_sales(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await state.update_data(position = callback.data)
    await state.set_state(DiagFSM.MODEL)
    try:
        await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    except:
        print("Не удалось изменить сообщение")
    await callback.message.answer(text="Какая основная модель продаж в Вашей компании?")
    await callback.message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_model_kb())

@diag_router.message(DiagFSM.POSITION, F.text)
async def model_of_sales(message: types.Message, state: FSMContext):
    await state.update_data(position = message.text)
    await state.set_state(DiagFSM.MODEL)
    # await message.edit_text(text=message.text, reply_markup=None)
    await message.answer(text="Какая основная модель продаж в Вашей компании?")
    await message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_model_kb())



@diag_router.callback_query(DiagFSM.MODEL)
async def field(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await state.update_data(model = callback.data)
    await state.set_state(DiagFSM.FIELD)
    try:
        await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    except:
        print("Не удалось изменить сообщение")
    await callback.message.answer(text="Какая основная модель продаж в Вашей компании?")
    await callback.message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_field_kb())

@diag_router.message(DiagFSM.MODEL, F.text)
async def field(message: types.Message, state: FSMContext):
    await state.update_data(model = message.text)
    await state.set_state(DiagFSM.FIELD)
    # await message.edit_reply_markup(reply_markup=None)
    await message.answer(text="Какая основная модель продаж в Вашей компании?")
    await message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_field_kb())



@diag_router.callback_query(DiagFSM.FIELD)
async def niche(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await state.update_data(field = callback.data)
    await state.set_state(DiagFSM.NICHE)
    try:
        await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    except:
        print("Не удалось изменить сообщение")
    await callback.message.answer(text="В какой  нише представлена Ваша компания?")
    await callback.message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_niche_kb())

@diag_router.message(DiagFSM.FIELD, F.text)
async def niche(message: types.Message, state: FSMContext):
    await state.update_data(field = message.text)
    await state.set_state(DiagFSM.NICHE)
    # await message.edit_reply_markup(reply_markup=None)
    await message.answer(text="В какой  нише представлена Ваша компания?")
    await message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_niche_kb())



@diag_router.callback_query(DiagFSM.NICHE)
async def service(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await state.update_data(niche = callback.data)
    await state.set_state(DiagFSM.SERVICE)
    try:
        await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    except:
        print("Не удалось изменить сообщение")
    await callback.message.answer(text="Укажите ключевой продукт или услугу Вашей компании")
    await callback.message.answer(text="Напишите текст в свободной форме")

@diag_router.message(DiagFSM.NICHE, F.text)
async def service(message: types.Message, state: FSMContext):
    
    await state.update_data(niche = message.text)
    await state.set_state(DiagFSM.SERVICE)
    # await message.edit_reply_markup(reply_markup=None)
    await message.answer(text="Укажите ключевой продукт или услугу Вашей компании")
    await message.answer(text="Напишите текст в свободной форме")



@diag_router.message(DiagFSM.SERVICE, F.text)
async def goal(message: types.Message, state: FSMContext):
    await state.update_data(service = message.text)
    await state.set_state(DiagFSM.GOAL)
    await message.answer(text="Укажите актуальную бизнес-задачу для решения которой Вы хотите обучиться.")
    await message.answer(text="Выберите варианты ниже или укажи текстом свою", reply_markup = inline.get_problem_kb())



@diag_router.callback_query(DiagFSM.GOAL)
async def problem(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await state.update_data(goal = callback.data)
    await state.set_state(DiagFSM.PROBLEM)
    try:
        await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    except:
        print("Не удалось изменить сообщение")
    await callback.message.answer(text="Сформулируйте четко в свободной форме самую актуальную проблему, которую  Вы хотели бы преодолеть в достижении текущей бизнес-задачи. Например: при холодных звонках не соединяют с ЛПР или другую")

@diag_router.message(DiagFSM.GOAL, F.text)
async def problem(message: types.Message, state: FSMContext):
    await state.update_data(goal = message.text)
    await state.set_state(DiagFSM.PROBLEM)
    # await message.edit_reply_markup(reply_markup=None)
    await message.answer(text="Сформулируйте четко в свободной форме самую актуальную проблему, которую  Вы хотели бы преодолеть в достижении текущей бизнес-задачи. Например: при холодных звонках не соединяют с ЛПР или другую")



@diag_router.message(DiagFSM.PROBLEM, F.text)
async def end_diag(message: types.Message, state: FSMContext):
    await state.update_data(problem = message.text)
    await state.set_state(DiagFSM.END_DIAG)
    await message.answer(text="Я успешно настроен для старта Вашего персонального обучения, нажмите продолжить чтобы получить список тем , в которые мы будем погружаться ближайший 21 день", reply_markup = inline.get_end_diag_kb())


def plan_formating(user_id: int)->str:
    plan_str = "Список тем для вашего обучения:\n\n"
    plan = db.get_plan(db.get_plan_id(user_id))
    plan = json.loads(plan)["data"]
    for n, theme in enumerate(plan):
        plan_str += f"{theme}\n\n"
    
    return plan_str



@diag_router.callback_query(DiagFSM.END_DIAG)
async def confirm_diag(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")
    await callback.message.answer(f"💬 {callback.data}")
    if callback.data == "Пройти заново":
        await state.set_state(DiagFSM.RESET)
        try:
            await callback.message.edit_text(text=callback.message.text, reply_markup=None)
        except:
            print("Не удалось изменить сообщение")
        await callback.message.answer(text="Вы уверены, что хотите сбросить настройки персонализации?", reply_markup=inline.get_reset_kb())

    if callback.data == "Продолжить":
        await callback.message.answer("Минутку, я подбираю Вам контент...")
        diag_data = await state.get_data()
        try:
        # await state.clear()
            plan = await get_course_plan(diag_data)
            db.insert_plan(db.get_user_id(callback.from_user.id), diag_data, plan)
            db.set_course(db.get_plan_id(db.get_user_id(callback.from_user.id)))
            plan_str = plan_formating(db.get_user_id(callback.from_user.id))
        except:
            with open("Logs.txt", "a", encoding = "utf-8") as f:
                f.write(f"{callback.from_user.id} ({callback.from_user.username}) Нет плана!!!!!\n")
            await callback.message.answer("Не удалось сгенерировать план под вашу диагностику, пройдите диагностику занаво, нажав /new или напишите в поддержку /support")
            await state.clear()
            return

        await state.set_state(CourseFSM.PLAN)
        try:
            await callback.message.edit_text(text=callback.message.text, reply_markup=None)
        except:
            print("Не удалось изменить сообщение")
        
        await callback.message.answer(plan_str)
        
        await callback.message.answer("Каждый день Вы будете получать обучающие материалы по теме дня", reply_markup=inline.get_start_course_kb())























#         plan = '''{"data": [
#   "Анализ рынка услуг в сфере кафе и ресторанов",
#   "Идентификация и привлечение целевой аудитории",
#   "Разработка уникального предложения на рынке",
#   "Продажи и маркетинг в B2B сфере",
#   "Разработка стратегии продаж для кафе и ресторанов",
#   "Методы увеличения среднего чека и частоты посещений",
#   "Анализ конкурентов и определение конкурентных преимуществ",
#   "Управление командой в сфере кафе и ресторанов",
#   "Мотивация персонала и увеличение эффективности работы",
#   "Управление рентабельностью в кафе и ресторанах",
#   "Финансовый анализ и планирование в сфере услуг",
#   "Управление запасами и снижение себестоимости продукции",
#   "Анализ и оптимизация рабочих процессов в кафе и ресторанах",
#   "Управление качеством обслуживания и удовлетворенностью клиентов",
#   "Эффективное использование рекламы и PR-активностей",
#   "Анализ эффективности маркетинговых каналов и инструментов",
#   "Продажи через партнеров и агентов в сфере услуг",
#   "Управление клиентскими отношениями и лояльностью",
#   "Применение CRM-систем для управления продажами",
#   "Анализ данных и принятие решений на основе аналитики",
#   "Развитие лидерских навыков для достижения целей"
# ]}'''