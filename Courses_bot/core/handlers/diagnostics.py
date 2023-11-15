from aiogram import Router
from aiogram import Bot, Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
from core.utils.fsm import DiagFSM, CourseFSM
from core.keyboards import inline
from core.utils.chatgpt import get_course_plan
from core.utils.database import db
diag_router = Router(name="diag")

@diag_router.callback_query(F.data == "diagnostics")
async def position(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(DiagFSM.POSITION)
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(text="Контент для какой компетенции Вам интересен?")
    await callback.message.answer(text="Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_position_kb())



@diag_router.callback_query(DiagFSM.POSITION)
async def model_of_sales(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(position = callback.data)
    await state.set_state(DiagFSM.MODEL)
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(text="Какая основная модель продаж в Вашей компании?")
    await callback.message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_model_kb())

@diag_router.message(DiagFSM.POSITION)
async def model_of_sales(message: types.Message, state: FSMContext):
    await state.update_data(position = message.text)
    await state.set_state(DiagFSM.MODEL)
    # await message.edit_text(text=message.text, reply_markup=None)
    await message.answer(text="Какая основная модель продаж в Вашей компании?")
    await message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_model_kb())



@diag_router.callback_query(DiagFSM.MODEL)
async def field(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(model = callback.data)
    await state.set_state(DiagFSM.FIELD)
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(text="Какая основная модель продаж в Вашей компании?")
    await callback.message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_field_kb())

@diag_router.message(DiagFSM.MODEL)
async def field(message: types.Message, state: FSMContext):
    await state.update_data(model = message.text)
    await state.set_state(DiagFSM.FIELD)
    # await message.edit_reply_markup(reply_markup=None)
    await message.answer(text="Какая основная модель продаж в Вашей компании?")
    await message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_field_kb())



@diag_router.callback_query(DiagFSM.FIELD)
async def niche(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(field = callback.data)
    await state.set_state(DiagFSM.NICHE)
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(text="В какой  нише представлена Ваша компания?")
    await callback.message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_niche_kb())

@diag_router.message(DiagFSM.FIELD)
async def niche(message: types.Message, state: FSMContext):
    await state.update_data(field = message.text)
    await state.set_state(DiagFSM.NICHE)
    # await message.edit_reply_markup(reply_markup=None)
    await message.answer(text="В какой  нише представлена Ваша компания?")
    await message.answer(text=" Выберите варианты ниже или укажи текстом свою", reply_markup=inline.get_niche_kb())



@diag_router.callback_query(DiagFSM.NICHE)
async def service(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(niche = callback.data)
    await state.set_state(DiagFSM.SERVICE)
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(text="Укажите ключевой продукт или услугу Вашей компании")
    await callback.message.answer(text="Напишите текст в свободной форме")

@diag_router.message(DiagFSM.NICHE)
async def service(message: types.Message, state: FSMContext):
    await state.update_data(niche = message.text)
    await state.set_state(DiagFSM.SERVICE)
    # await message.edit_reply_markup(reply_markup=None)
    await message.answer(text="Укажите ключевой продукт или услугу Вашей компании")
    await message.answer(text="Напишите текст в свободной форме")



@diag_router.message(DiagFSM.SERVICE)
async def goal(message: types.Message, state: FSMContext):
    await state.update_data(service = message.text)
    await state.set_state(DiagFSM.GOAL)
    await message.answer(text="Укажите актуальную бизнес-задачу для решения которой Вы хотите обучиться.")
    await message.answer(text="Выберите варианты ниже или укажи текстом свою", reply_markup = inline.get_problem_kb())



@diag_router.callback_query(DiagFSM.GOAL)
async def problem(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(goal = callback.data)
    await state.set_state(DiagFSM.PROBLEM)
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(text="Сформулируйте четко в свободной форме самую актуальную проблему, которую  Вы хотели бы преодолеть в достижении текущей бизнес-задачи. Например: при холодных звонках не соединяют с ЛПР или другую")

@diag_router.message(DiagFSM.GOAL)
async def problem(message: types.Message, state: FSMContext):
    await state.update_data(goal = message.text)
    await state.set_state(DiagFSM.PROBLEM)
    # await message.edit_reply_markup(reply_markup=None)
    await message.answer(text="Сформулируйте четко в свободной форме самую актуальную проблему, которую  Вы хотели бы преодолеть в достижении текущей бизнес-задачи. Например: при холодных звонках не соединяют с ЛПР или другую")



@diag_router.message(DiagFSM.PROBLEM)
async def end_diag(message: types.Message, state: FSMContext):
    await state.update_data(problem = message.text)
    await state.set_state(DiagFSM.END_DIAG)
    await message.answer(text="Я успешно настроен для старта Вашего персонального обучения, нажмите продолжить чтобы получить список тем , в которые мы будем погружаться ближайший 21 день", reply_markup = inline.get_end_diag_kb())




@diag_router.callback_query(DiagFSM.END_DIAG)
async def confirm_diag(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Пройти заново":
        await state.set_state(DiagFSM.RESET)
        await callback.message.edit_text(text=callback.message.text, reply_markup=None)
        await callback.message.answer(text="Вы уверены, что хотите сбросить настройки персонализации?", reply_markup=inline.get_reset_kb())

    if callback.data == "Продолжить":
        diag_data = await state.get_data()
        await state.clear()
        plan = await get_course_plan(diag_data)
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
        db.insert_plan(db.get_user_id(callback.from_user.id), diag_data, plan)
        db.set_course(db.get_plan_id(db.get_user_id(callback.from_user.id)))
        


        await state.set_state(CourseFSM.PLAN)
        await callback.message.edit_text(text=callback.message.text, reply_markup=None)
        
        await callback.message.answer("Каждый день Вы будете получать обучающие материалы по теме дня", reply_markup=inline.get_start_course_kb())






















