from aiogram import Router
from aiogram import Bot, Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
import json
from core.utils.fsm import DiagFSM, CourseFSM
from core.keyboards import inline
from core.utils.database import is_subscribed
from core.handlers.diagnostics import position 
from core.utils.chatgpt import get_lecture_gpt, get_feedback_gpt, get_frameworks_gpt, get_advices_gpt, get_exercises_gpt, get_reflex_gpt
from core.utils.database import db

course_router = Router()

# @course_router.callback_query(DiagFSM.END_DIAG)
# async def confirm_diag(callback: types.CallbackQuery, state: FSMContext):
#     if callback.data == "Продолжить":
#         insert_diag()
#         await state.clear()
#     if callback.data == "Пройти заново":
#         await state.set_state(DiagFSM.RESET)
#         await callback.message.answer(text="Вы уверены, что хотите сбросить настройки персонализации?", reply_markup=inline.get_reset_kb())

@course_router.callback_query(DiagFSM.RESET)
async def reset_diag(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    if callback.data == "Да":
        await state.clear()
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except:
            print("Не удалось изменить кнопки")
        await position(callback=callback, state=state)
        
    if callback.data == "Нет":
        await state.set_state(DiagFSM.END_DIAG)
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except:
            print("Не удалось изменить кнопки")
        await callback.message.answer(text="Я успешно настроен для старта Вашего персонального обучения, нажмите продолжить чтобы получить список тем , в которые мы будем погружаться ближайший 21 день", reply_markup = inline.get_end_diag_kb())


@course_router.callback_query(CourseFSM.PLAN)
async def start_course(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await callback.message.answer("Минутку, я подбираю Вам контент...")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")
    await state.set_state(CourseFSM.LECTURE)
    try:
        day = db.get_day(callback.from_user.id) - 1
        lesson = db.get_plan(db.get_plan_id(db.get_user_id(callback.from_user.id)))
        lesson = json.loads(lesson)["data"][day]
        diag = db.get_diag(db.get_latest_course(db.get_user_id(callback.from_user.id)))

        lecture = await get_lecture_gpt(lesson, diag)
        # lecture = "лекция"
        await state.update_data(context = lecture)
        await callback.message.answer(lecture, reply_markup=inline.get_lecture_kb())
        db.update_day_status(db.get_latest_course(db.get_user_id(callback.from_user.id)), "lecture")
    except:
        await callback.message.answer("Что-то пошло не так", reply_markup=inline.get_lecture_kb())


@course_router.callback_query(CourseFSM.BEFORE_FRAMEWORKS)
async def framework_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await callback.message.answer("Минутку, я подбираю Вам контент...")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")
    await state.set_state(CourseFSM.FRAMEWORKS)
    try:
        day = db.get_day(callback.from_user.id) - 1
        lesson = db.get_plan(db.get_plan_id(db.get_user_id(callback.from_user.id)))
        lesson = json.loads(lesson)["data"][day]
        diag = db.get_diag(db.get_latest_course(db.get_user_id(callback.from_user.id)))

                
        frameworks = await get_frameworks_gpt(lesson, diag)
        # frameworks = "фреймворки"

        await state.update_data(context = frameworks)
        await callback.message.answer(text=frameworks, reply_markup=inline.get_frameworks_kb())
        db.update_day_status(db.get_latest_course(db.get_user_id(callback.from_user.id)), "frameworks")
    except:
        await callback.message.answer("Что-то пошло не так", reply_markup=inline.get_frameworks_kb())

@course_router.callback_query(CourseFSM.LECTURE)
async def frameworks(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await callback.message.answer("Минутку, я подбираю Вам контент...")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")

    if callback.data == "Подробнее":
        await state.set_state(CourseFSM.FEEDBACK_LECTURE)
        await callback.message.answer("Сформулируйте четкий вопрос. Например: “хочу узнать более подробно про технику преодоления барьеров в продажах”")
        return

    if callback.data == "Далее: Фреймворки":
        await state.set_state(CourseFSM.BEFORE_FRAMEWORKS)
        await framework_answer(callback = callback, state = state)

@course_router.message(CourseFSM.FEEDBACK_LECTURE, F.text)
async def feedback_lecture(message: types.Message, state: FSMContext):
    await message.answer("Минутку...")
    data = await state.get_data()
    try:
        feedback = await get_feedback_gpt(context = data["context"], question = message.text)
    except:
        feedback = "не удалось сгенерировать ответ на ваш вопрос"
    await state.set_state(CourseFSM.BEFORE_FRAMEWORKS)
    await message.answer(feedback, reply_markup=inline.get_before_frameworks_kb())


@course_router.callback_query(CourseFSM.FRAMEWORKS)
async def advices(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await callback.message.answer("Минутку, я подбираю Вам контент...")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")

    if callback.data == "Подробнее":
        await state.set_state(CourseFSM.FEEDBACK_FRAMEWORKS)
        await callback.message.answer("Сформулируйте четкий вопрос. Например: “хочу узнать более подробно про технику преодоления барьеров в продажах”")
        return

    if callback.data == "Далее: Советы":
        await advices_answer(callback = callback, state = state)



@course_router.message(CourseFSM.FEEDBACK_FRAMEWORKS, F.text)
async def feedback_frameworks(message: types.Message, state: FSMContext):
    await message.answer("Минутку...")
    data = await state.get_data()
    try:
        feedback = await get_feedback_gpt(context = data["context"], question = message.text)
    except:
        feedback = "не удалось сгенерировать ответ на ваш вопрос"
    await state.set_state(CourseFSM.BEFORE_ADVICES)
    await message.answer(feedback, reply_markup=inline.get_before_advices_kb())

@course_router.callback_query(CourseFSM.BEFORE_ADVICES)
async def advices_answer(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")
    if is_subscribed(1):
        await state.set_state(CourseFSM.ADVICES)
        try:
            day = db.get_day(callback.from_user.id) - 1
            lesson = db.get_plan(db.get_plan_id(db.get_user_id(callback.from_user.id)))
            lesson = json.loads(lesson)["data"][day]
            diag = db.get_diag(db.get_latest_course(db.get_user_id(callback.from_user.id)))
            try:
                advices = await get_advices_gpt(lesson, diag)
                # aadvices ="Советы"
                
            except:
                advices = "Не удалось сгенерировать советы"
            await callback.message.answer(text=advices, reply_markup=inline.get_ex_kb())
            db.update_day_status(db.get_latest_course(db.get_user_id(callback.from_user.id)), "advices")
            return
        except:
            await callback.message.answer("Что-то пошло не так", reply_markup=inline.get_ex_kb())
    else:
        await callback.message.answer("Вы завершили ознакомительную версию. Для продолжения погружения в обучающую программу, пожалуйста оплатите доступ. Привлечение финансов позволяет развивать продукт и делать его еще более совершенным.")
        await callback.message.answer("Что Вас ждет в платном доступе: \n1. 3 недели интенсива по индивидуальному плану обучения.\n2. Теоретические и практические материалы для эффективного погружения и повышения своего уровня компетенции.\3. Фреймворки, модели, рабочие инструменты и практические советы чтобы стать специалистом высокого уровня на своем рабочем месте.\nДо 10 дополнительных вопросов по теме.\nДо 10 новых курсов в подборке")
        await state.set_state(CourseFSM.BEFORE_ADVICES)
        await callback.message.answer("Здесь производится оплата тарифа", reply_markup=inline.get_before_advices_kb())


@course_router.callback_query(CourseFSM.ADVICES)
async def exercises(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await callback.message.answer("Минутку, я подбираю Вам контент...")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")
    await state.set_state(CourseFSM.EXERCISES)
    try:
        day = db.get_day(callback.from_user.id) - 1
        lesson = db.get_plan(db.get_plan_id(db.get_user_id(callback.from_user.id)))
        lesson = json.loads(lesson)["data"][day]
        diag = db.get_diag(db.get_latest_course(db.get_user_id(callback.from_user.id)))
        exercises = await get_exercises_gpt(lesson, diag)
        # exercises = "упражнения"
    except:
        exercises = "Не удалось сгенерировать задания"
    
    await callback.message.answer(exercises, reply_markup=inline.get_reflex_kb())
    db.update_day_status(db.get_latest_course(db.get_user_id(callback.from_user.id)), "exercises")
    

@course_router.callback_query(CourseFSM.EXERCISES)
async def reflex(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    await callback.message.answer("Минутку, я подбираю Вам контент...")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")
    await state.set_state(CourseFSM.REFLEX)
    try:
        day = db.get_day(callback.from_user.id) - 1
        lesson = db.get_plan(db.get_plan_id(db.get_user_id(callback.from_user.id)))
        lesson = json.loads(lesson)["data"][day]
        diag = db.get_diag(db.get_latest_course(db.get_user_id(callback.from_user.id)))
        reflex = await get_reflex_gpt(lesson, diag)
        # reflex = "рефлексия"
    except: 
        reflex = "Не удалось сгенерировать рефлексию"

    await callback.message.answer(reflex)
    await state.clear()
    db.update_day_status(db.get_latest_course(db.get_user_id(callback.from_user.id)), "end")
    if day < 20:
        db.update_day(db.get_latest_course(db.get_user_id(callback.from_user.id)), day+1)
    else:
        db.update_course_status(db.get_latest_course(db.get_user_id(callback.from_user.id)), "end")
    await callback.message.answer("Не забывай сохранять записи своей рефлексии. Они пригодятся для последующего грамотного формирования новых обучающих программ.")
    await callback.message.answer("Надеюсь сегодня было полезно. До завтра", reply_markup = inline.get_next_menu_theme_kb())


@course_router.callback_query(F.data =="Следующая тема")
async def continue_lesson(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f"💬 {callback.data}")
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except:
        print("Не удалось изменить кнопки")
    
    await state.clear()
    if db.get_course_status(db.get_latest_course(db.get_user_id(callback.from_user.id))) == "end":
        await callback.message.answer("Данный курс кончился. Вы можете начать новый, пользуясь командой в меню.", reply_markup=inline.get_next_menu_kb())
        return
    day_status = db.get_day_status(callback.from_user.id)
    if day_status=="end":
        await callback.message.answer("Начинаем новый урок!")
        await start_course(callback=callback, state=state)
    else:
        await callback.message.answer("Чтобы начать новый урок, нужно сначала закончить старый")
        if  day_status== "started" or day_status=="lecture":
            await start_course(callback=callback, state=state)
        elif day_status=="frameworks":
            await framework_answer(callback=callback, state=state)
        elif day_status == "advices":
            await advices_answer(callback=callback, state=state)
        elif day_status == "exercises":
            await exercises(callback=callback, state=state)
        else:
            await callback.answer("Что-то пошло не так. Попробуйте выбрать новый курс или продолжить текущий в меню.")