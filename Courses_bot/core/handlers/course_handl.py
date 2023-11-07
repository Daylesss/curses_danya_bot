from aiogram import Router
from aiogram import Bot, Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
from core.utils.fsm import DiagFSM, CourseFSM
from core.keyboards import inline
from core.utils.database import insert_diag, on_course, get_lesson, is_subscribed
from core.handlers.diagnostics import position 
from core.utils.chatgpt import get_lecture_gpt, get_feedback_gpt, get_frameworks_gpt, get_advices_gpt, get_exercises_gpt, get_reflex_gpt

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
    if callback.data == "Да":
        await state.clear()
        await position(callback=callback, state=state)
        
    if callback.data == "Нет":
        await state.set_state(DiagFSM.END_DIAG)
        await callback.message.answer(text="Я успешно настроен для старта Вашего персонального обучения, нажмите продолжить чтобы получить список тем , в которые мы будем погружаться ближайший 21 день", reply_markup = inline.get_end_diag_kb())


@course_router.callback_query(CourseFSM.PLAN)
async def start_course(callback: types.CallbackQuery, state: FSMContext):
    on_course()
    lesson = get_lesson(0)
    
    lecture = await get_lecture_gpt(lesson)
    await state.set_state(CourseFSM.LECTURE)
    await state.update_data(lecture = lecture)
    await callback.message.answer(lecture, reply_markup=inline.get_lecture_kb())


@course_router.callback_query(CourseFSM.BEFORE_FRAMEWORKS)
async def framework_answer(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CourseFSM.FRAMEWORKS)
    lesson = get_lesson(0)
            
    frameworks = await get_frameworks_gpt(lesson)
    await state.update_data(frameworks = frameworks)
    await callback.message.answer(text=frameworks, reply_markup=inline.get_frameworks_kb())

@course_router.callback_query(CourseFSM.LECTURE)
async def frameworks(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Подробнее":
        await state.set_state(CourseFSM.FEEDBACK_LECTURE)
        await callback.message.answer("Сформулируйте четкий вопрос. Например: “хочу узнать более подробно про технику преодоления барьеров в продажах”")
        return

    if callback.data == "Далее: Фреймворки":
        await framework_answer(callback = callback, state = state)
        # lesson = await get_lesson(0)
        
        # frameworks = await get_frameworks_gpt(lesson)
        # await state.update_data(frameworks = frameworks)
        # await callback.message.answer(text=frameworks, reply_markup=inline.get_frameworks_kb())

@course_router.message(CourseFSM.FEEDBACK_LECTURE)
async def feedback_lecture(message: types.Message, state: FSMContext):
    data = await state.get_data()
    feedback = await get_feedback_gpt(context = data["lecture"], question = message.text)
    await state.set_state(CourseFSM.BEFORE_FRAMEWORKS)
    await message.answer(feedback, reply_markup=inline.get_before_frameworks_kb())


@course_router.callback_query(CourseFSM.FRAMEWORKS)
async def frameworks(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Подробнее":
        await state.set_state(CourseFSM.FEEDBACK_FRAMEWORKS)
        await callback.message.answer("Сформулируйте четкий вопрос. Например: “хочу узнать более подробно про технику преодоления барьеров в продажах”")
        return

    if callback.data == "Далее: Фреймворки":
        await framework_answer(callback = callback, state = state)


@course_router.message(CourseFSM.FEEDBACK_FRAMEWORKS)
async def feedback_frameworks(message: types.Message, state: FSMContext):
    data = await state.get_data()
    feedback = await get_feedback_gpt(context = data["frameworks"], question = message.text)
    await state.set_state(CourseFSM.BEFORE_ADVICES)
    await message.answer(feedback, reply_markup=inline.get_before_advices_kb())

@course_router.callback_query(CourseFSM.BEFORE_ADVICES)
async def framework_answer(callback: types.CallbackQuery, state: FSMContext):

    if is_subscribed(1):
        lesson = get_lesson(0)   
        await state.clear()
        await state.set_state(CourseFSM.ADVICES)
                
        advices = await get_advices_gpt(lesson)
        await callback.message.answer(text=advices, reply_markup=inline.get_ex_kb())
        
        return
    else:
        await callback.message.answer("Вы завершили ознакомительную версию. Для продолжения погружения в обучающую программу, пожалуйста оплатите доступ. Привлечение финансов позволяет развивать продукт и делать его еще более совершенным.")
        await callback.message.answer("Что Вас ждет в платном доступе: \n1. 3 недели интенсива по индивидуальному плану обучения.\n2. Теоретические и практические материалы для эффективного погружения и повышения своего уровня компетенции.\3. Фреймворки, модели, рабочие инструменты и практические советы чтобы стать специалистом высокого уровня на своем рабочем месте.\nДо 10 дополнительных вопросов по теме.\nДо 10 новых курсов в подборке")
        await state.set_state(CourseFSM.BEFORE_ADVICES)
        await callback.message.answer("Здесь производится оплата тарифа", reply_markup=inline.get_before_advices_kb())


@course_router.callback_query(CourseFSM.ADVICES)
async def exercises(callback: types.CallbackQuery, state: FSMContext):
    lesson = get_lesson(0)
    await state.set_state(CourseFSM.EXERCISES)
    exercises = await get_exercises_gpt(lesson)
    
    await callback.message.answer(exercises, reply_markup=inline.get_reflex_kb())
    

@course_router.callback_query(CourseFSM.EXERCISES)
async def reflex(callback: types.CallbackQuery, state: FSMContext):
    lesson = get_lesson(0)
    await state.set_state(CourseFSM.REFLEX)
    reflex = await get_reflex_gpt(lesson)
    
    await callback.message.answer(reflex)
    await state.clear()
    await callback.message.answer("Не забывай сохранять записи своей рефлексии. Они пригодятся для последующего грамотного формирования новых обучающих программ.")
    await callback.message.answer("Надеюсь сегодня было полезно. До завтра", reply_markup = inline.get_next_menu_kb())
    
