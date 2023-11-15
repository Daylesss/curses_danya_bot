from aiogram import Router
from aiogram import Bot, Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
import os
from dotenv import load_dotenv, find_dotenv
from core.utils.fsm import BaseFSM
from core.utils.commands import set_command
from core.keyboards import inline
from core.handlers.diagnostics import position
from core.utils.database import db
from core.utils.other import get_courses_message
from core.handlers.course_handl import start_course

load_dotenv(find_dotenv())

base_router = Router(name="Main")


@base_router.startup()
async def start_bot(bot: Bot):
    await set_command(bot)
    await bot.send_message(os.getenv('ADMIN'), "Courses bot started.")

@base_router.shutdown()
async def stop_bot(bot:Bot):
    await bot.send_message(os.getenv('ADMIN'), "Courses bot stopped.")


@base_router.callback_query(F.data == "menu")
async def menu(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BaseFSM.MENU)
    await callback.message.delete()
    await callback.message.answer("Здесь вы можете управлять своими курсами", reply_markup=inline.get_menu_kb())






@base_router.callback_query(BaseFSM.MENU, F.data == "Об обучении")
async def about(callback:types.CallbackQuery, state: FSMContext):
    await state.set_state(BaseFSM.ABOUT)
    await callback.message.edit_reply_markup(reply_markup=inline.get_about_kb())


@base_router.callback_query(BaseFSM.ABOUT, F.data == "Как правильно учиться")
async def about(callback:types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('''Понимание и усвоение теории может потребовать времени и усилий, особенно если материал сложен или незнаком. Чтобы правильно и эффективно вникать в теорию, рекомендую следовать следующим шагам:
Подготовьте рабочее пространство: Убедитесь, что у вас есть комфортное и тихое место для учебы, минимизируйте отвлекающие факторы.
Обзор материала: Прежде чем глубоко погружаться в тему, дайте себе общее представление о том, что перед вами. Это поможет установить контекст и определить ключевые моменты.
Разделите на части: Не пытайтесь усвоить все сразу. Разбейте материал на управляемые части и изучайте их по отдельности.
Создайте свои заметки: Письмо помогает запомнить информацию. Делая заметки, вы также переформулируете материал своими словами, что улучшает понимание.
Обсуждайте с другими: Обсуждение материала с коллегами или друзьями может выявить непонятные моменты и помочь усвоить информацию.
Применяйте на практике: Если это возможно, попробуйте применить теорию на практике. Экспериментирование или выполнение практических заданий поможет лучше понять материал.
Пересматривайте материал: Периодически возвращайтесь к изученному, чтобы освежить свои знания и закрепить их.
Дайте себе время: Усвоение сложной теории требует времени. Не пытайтесь спешить, дайте себе время на размышления и понимание.
Создайте ассоциации: Связывание новой информации с уже известной поможет легче ее запомнить и понять.
Помните, что у каждого свой темп и стиль обучения. Главное — это находить радость и интерес в процессе погружения в новую теорию и не бояться задавать вопросы.''', reply_markup=inline.get_about_kb())


@base_router.callback_query(BaseFSM.ABOUT, F.data == "Как работать с фреймворками")
async def about(callback:types.CallbackQuery, state: FSMContext):
    # await state.set_state(BaseFSM.MENU)
    await callback.message.edit_text('''Фреймворк — это как рецепт или набор инструкций, который показывает, как делать что-то сложное шаг за шагом. Вместо того чтобы каждый раз придумывать, как готовить блюдо, вы следуете проверенному рецепту. Точно так же, вместо того чтобы создавать что-то с нуля в бизнесе или технологиях, вы можете использовать фреймворк как ваш рецепт или инструкцию. Вот несколько шагов и рекомендаций по правильной работе с фреймворком:
Изучение фреймворка: Перед тем как начать работу, потратьте время на изучение фреймворка. Понимание его основных компонентов, функций и принципов работы поможет вам использовать его наиболее эффективно.
Следование рекомендациям: Фреймворки обычно снабжены руководствами и рекомендациями по использованию. Эти руководства помогут вам избежать типичных ошибок.
Настройка под свои нужды: Хотя фреймворк предоставляет базовую структуру, он часто гибок и может быть адаптирован под конкретные нужды вашего бизнеса.
Обновление: Как и любой другой инструмент или программное обеспечение, фреймворки регулярно обновляются. Следите за этими обновлениями, чтобы использовать последние возможности и исправления.
Сообщество: Многие популярные фреймворки имеют большие сообщества пользователей. Участие в таких сообществах может предоставить вам дополнительные ресурсы, советы и решения для возникающих проблем.
Тестирование: При внедрении или изменении фреймворка всегда проводите тесты. Это поможет обнаружить и устранить ошибки до того, как они станут проблемой.
Отзывчивость: Будьте готовы к изменениям. Фреймворк может потребовать корректировки или адаптации по мере развития вашего бизнеса.
Ключ к успешной работе с фреймворком — это его понимание, гибкость в использовании и готовность к обучению и адаптации.''', reply_markup=inline.get_about_kb())
    

@base_router.callback_query(BaseFSM.ABOUT, F.data == "Как применять знания на практике")
async def about(callback:types.CallbackQuery, state: FSMContext):
    # await state.set_state(BaseFSM.MENU)
    await callback.message.edit_text('''Эффективное применение знаний на практике в работе - это ключевой элемент профессионального роста и успешной деятельности. Вот несколько советов, как это сделать:
Определите приоритеты. Определите, какие из ваших знаний являются наиболее ценными для вашей текущей позиции и задач.
Постоянное обучение. Постоянно ищите возможности для обучения и развития. Это может быть чтение книг, участие в вебинарах, курсах или мастер-классах.
Применяйте теорию на практике. Попробуйте внедрить новые идеи или методы в свою ежедневную работу. Экспериментирование помогает понять, что работает, а что нет.
Обсуждение с коллегами. Делитесь своими знаниями и обсуждайте их с коллегами. Они могут предложить новые точки зрения или подходы, о которых вы не думали.
Документирование. Записывайте свои мысли, идеи и процессы. Это не только помогает фиксировать знания, но и позволяет вернуться к ним, когда это будет необходимо.
Отражение. Посвящайте время самоанализу. Задавайте себе вопросы: "Что я сделал правильно?", "Что мог бы сделать лучше?", "Какие уроки я извлек?".
Задайте себе цели. Установите четкие, измеримые цели на короткий и долгосрочный периоды. Это поможет направить ваши усилия и знания в нужном направлении.
Запрашивайте обратную связь. Прошу коллег или руководителя дать вам обратную связь по вашей работе. Это может помочь увидеть области, в которых вам стоит улучшить свои навыки или знания.
Применяйте критическое мышление. Прежде чем принимать решения на основе своих знаний, проанализируйте информацию с разных точек зрения.
Будьте гибкими. Мир и рынок труда постоянно меняются. Будьте готовы адаптировать свои знания и навыки под новые условия и требования.
В заключение, главное — это применять знания на практике, не бояться ошибок и учиться на них, а также постоянно стремиться к развитию и совершенствованию своих навыков.''', reply_markup=inline.get_about_kb())


@base_router.callback_query(BaseFSM.ABOUT, F.data == "Как проводить рефлексию")
async def about(callback:types.CallbackQuery, state: FSMContext):
    # await state.set_state(BaseFSM.MENU)
    await callback.message.edit_text('''Рефлексия — это процесс самонаблюдения и анализа собственных действий, чувств и мыслей. Рефлексивная практика может помочь вам лучше понимать себя, улучшить навыки принятия решений и улучшить отношения с другими. Вот несколько рекомендаций по работе с рефлексией:
Время и место. Уделите специальное время для рефлексии, предпочтительно в тихом месте, где вас ничто не отвлекает. Это может быть конец рабочего дня, недели или после важного события.
Записывайте свои мысли. Ведите дневник рефлексии или журнал, где будете записывать свои размышления. Это поможет вам увидеть динамику своего развития и замечать рекуррентные паттерны в поведении (повторяющиеся привычки или реакции, которые человек демонстрирует в определенных ситуациях. Это похоже на то, как некоторые из нас автоматически проверяют телефон, когда у них есть свободная минута, или на то, как некоторые люди всегда заказывают одно и то же блюдо в ресторане).
Поставьте себе вопросы. Например: "Что произошло?", "Как я на это реагировал?", "Почему я так поступил?", "Что я чувствовал?", "Что бы я мог сделать по-другому?", "Что я из этого узнал?".
Будьте честными с собой. Рефлексия требует искренности. Признавайте свои ошибки и достижения.
Применяйте методы глубокой рефлексии. Например, можно использовать метод "шесть шляп мышления" Эдварда де Боно или SWOT-анализ для анализа собственных сильных и слабых сторон, возможностей и угроз.
Обсудите свои размышления с другими. Разговаривайте с коллегами, наставниками или друзьями. Они могут предоставить вам другую перспективу или помочь увидеть то, что вы пропустили.
Применяйте полученные знания на практике. Рефлексия должна вести к личному и профессиональному росту. Ставьте перед собой новые задачи и пробуйте новые подходы на основе своих размышлений.
Продолжайте обучение. Чтение книг, посещение тренингов, участие в мастер-классах может стать отличным стимулом для рефлексии и позволит углубиться в процесс самоанализа.
Не критикуйте себя слишком строго. Рефлексия — это инструмент для развития, а не самокритики. Если вы находите что-то, что хотели бы изменить в себе, рассматривайте это как возможность для роста, а не как недостаток.
Применяйте медитацию и медленное дыхание. Эти практики помогут вам расслабиться, сконцентрироваться на своих чувствах и мыслях и углубить процесс рефлексии.
Важно помнить, что рефлексия — это непрерывный процесс. Чем больше вы практикуетесь, тем легче будет анализировать свои действия и находить пути к личному и профессиональному росту.''', reply_markup=inline.get_about_kb())





@base_router.callback_query(BaseFSM.MENU, F.data == "Начать новое обучение")
async def about(callback:types.CallbackQuery, state: FSMContext):
    await state.set_state(BaseFSM.NEW)
    await callback.message.answer("Вы уверены, что хотите начать новый курс обучения и сбросить настройки персонализации? Текущий прогресс будет утерян.", reply_markup=inline.get_reset_kb())
    


@base_router.callback_query(BaseFSM.NEW)
async def reset_diag(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "Да":
        await state.clear()
        await position(callback=callback, state=state)
        
    if callback.data == "Нет":
        await state.clear()
        await callback.message.edit_reply_markup(reply_markup=inline.get_next_menu_kb())


@base_router.callback_query(BaseFSM.MENU, F.data == "Поддержка")
async def support(callback:types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Ваши предложения, пожелания и вопросы вы можете написать в телеграмм @monoqle_support", reply_markup=inline.get_next_menu_kb())


@base_router.callback_query(BaseFSM.MENU, F.data == "Мои курсы")
async def my_courses(callback:types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(BaseFSM.COURSES)
    await callback.message.answer("Продолжить прохождение текущего курса или выбрать новый", reply_markup=inline.get_choice_course_kb())

@base_router.callback_query(BaseFSM.COURSES, F.data == "Продолжить")
async def continue_course(callback:types.CallbackQuery, state: FSMContext):
    await state.set_state(BaseFSM.THIS_COURSE)
    await callback.message.answer("Начать текущий урок?", reply_markup=inline.get_this_lesson_kb())

@base_router.callback_query(BaseFSM.THIS_COURSE, F.data == "Да")
async def start_this_lesson(callback:types.CallbackQuery, state: FSMContext):
    await state.clear()
    if db.get_course_status(db.get_latest_course(db.get_user_id(callback.from_user.id))) == "end":
        await callback.message.answer("Данный курс кончился", reply_markup=inline.get_next_menu_kb())
        return
    day_status = db.get_day_status(callback.from_user.id)
    if day_status == "end":
        await callback.message.answer("Вы уже прошли сегодняшний день. Ожидайте следующее сообщение в 10:00 по Мск", reply_markup=inline.get_next_menu_kb())
    else:
        await start_course(callback = callback, state = state)

@base_router.callback_query(BaseFSM.COURSES, F.data == "Выбрать")
async def all_courses(callback:types.CallbackQuery, state: FSMContext):
    await state.set_state(BaseFSM.CHOICE_COURSES)
    dict_cousres = get_courses_message(db.get_user_id(callback.from_user.id))
    msg = ""
    for course in dict_cousres.values():
        msg += course[1]
    await callback.message.edit_text(msg, reply_markup=None)
    await callback.message.answer("Введите номер курса, который вы хотите выбрать\nНапример: 3", reply_markup=inline.get_next_menu_kb())

@base_router.message(BaseFSM.CHOICE_COURSES)
async def choice_course(message: types.Message, state: FSMContext):
    dict_cousres = get_courses_message(db.get_user_id(message.from_user.id))
    if 0 < int(message.text) < len(dict_cousres) + 1:
        if db.get_course_status(dict_cousres[int(message.text)][0]) != "end":
            db.upd_latest_course(message.from_user.id, dict_cousres[int(message.text)][0])
            await state.clear()
            await message.answer("Курс успешно обновлен", reply_markup=inline.get_next_menu_kb())
        else: 
            await state.clear()
            await message.answer("Этот курс уже закончен или его не существует", inline.get_next_menu_kb())
    else:
        await state.clear()
        await message.answer("Введите корректный номер курса")
        await state.clear()
        await state.set_state(BaseFSM.CHOICE_COURSES)
        dict_cousres = get_courses_message(db.get_user_id(message.from_user.id))
        msg = ""
        for course in dict_cousres.values():
            msg += course[1]
        await message.answer(msg, reply_markup=None)
        await message.answer("Введите номер курса, который вы хотите выбрать\nНапример: 3", reply_markup=inline.get_next_menu_kb())
            