from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_start_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="К диагностике", callback_data="К диагностике")
    builder.button(text="Меню", callback_data="Меню")
    
    builder.adjust(1, 1)
    
    return builder.as_markup()

def get_position_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Генеральный директор", callback_data="Генеральный директор")
    builder.button(text="Руководитель отдела продаж", callback_data="Руководитель отдела продаж")
    builder.button(text="Менеджер отдела продаж", callback_data="Менеджер отдела продаж")
    builder.button(text="Менеджер по работе с клиентами", callback_data="Менеджер по работе с клиентами")
    builder.button(text="Менеджер по маркетингу и рекламе", callback_data="Менеджер по маркетингу и рекламе")
    builder.button(text="Менеджер по персоналу", callback_data="Менеджер по персоналу")
    builder.button(text="Менеджер по логистике", callback_data="Менеджер по логистике")
    builder.button(text="Менеджер интернет-магазина", callback_data="Менеджер интернет-магазина")
    builder.button(text="Контент-менеджер", callback_data="Контент-менеджер")
    builder.button(text="SMM-специалист", callback_data="SMM-специалист")
    
    # builder.button(text="", callback_data="User_position")
    
    builder.adjust(1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    
    return builder.as_markup()

def get_model_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="B2B (Мы продаем компаниям)", callback_data="B2B")
    builder.button(text="B2C (Мы продаем людям)", callback_data="B2C")
    builder.button(text="B2B2C (Мы продаем компаниям, которые продают людям)", callback_data="B2B2C")
    
    # builder.button(text="", callback_data="User_position")
    
    builder.adjust(1, 1, 1)
    
    return builder.as_markup()

def get_field_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Торговля", callback_data="Торговля")
    builder.button(text="Услуги", callback_data="Услуги")
    builder.button(text="Общественное питание", callback_data="Общественное питание")
    builder.button(text="Консалтинг", callback_data="Консалтинг")


    
    # builder.button(text="", callback_data="User_position")
    
    builder.adjust(1, 1, 1, 1)
    
    return builder.as_markup()

def get_niche_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Кафе, рестораны", callback_data="Кафе, рестораны")
    builder.button(text="Отели", callback_data="Отели")
    builder.button(text="Бьюти", callback_data="Бьюти индустрия")
    builder.button(text="IT", callback_data="IT")
    builder.button(text="Строительство", callback_data="Строительство")
    builder.button(text="Логистика", callback_data="Логистика")
    builder.button(text="Сельское хозяйство", callback_data="Сельское хозяйство")

    builder.adjust(1, 1, 1, 1, 1, 1, 1)
    
    return builder.as_markup()

def get_problem_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Повышение продаж", callback_data="Повышение продаж")
    builder.button(text="Улучшение конверсий холодных звонков", callback_data="холодных звонков")
    builder.button(text="Качество коммуникаций с клиентами", callback_data="коммуникаций с клиентами")
    builder.button(text="Качество коммуникаций с коллегами", callback_data="коммуникаций с коллегами")


    builder.adjust(1, 1, 1, 1)
    
    return builder.as_markup()

def get_end_diag_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Продолжить", callback_data="Продолжить")
    builder.button(text="Пройти заново", callback_data="Пройти заново")


    builder.adjust(1, 1)
    
    return builder.as_markup()

def get_reset_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Да", callback_data="Да")
    builder.button(text="Нет", callback_data="Нет")


    builder.adjust(2)
    
    return builder.as_markup()


def get_start_course_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Начать обучение", callback_data="Начать обучение")

    builder.adjust(1)
    
    return builder.as_markup()


def get_lecture_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Подробнее", callback_data="Подробнее")
    builder.button(text="Далее: Фреймворки", callback_data="Далее: Фреймворки")

    builder.adjust(1,1)
    
    return builder.as_markup()

def get_frameworks_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Подробнее", callback_data="Подробнее")
    builder.button(text="Далее: Советы", callback_data="Далее: Советы")

    builder.adjust(1,1)
    
    return builder.as_markup()

def get_before_frameworks_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Далее: Фреймворки", callback_data="Далее: Фреймворки")

    builder.adjust(1)
    
    return builder.as_markup()

def get_before_advices_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Далее: Советы", callback_data="Далее: Советы")

    builder.adjust(1)
    
    return builder.as_markup()

def get_ex_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Далее: Задания", callback_data="Далее: Задания")

    builder.adjust(1)
    
    return builder.as_markup()

def get_reflex_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Далее: Рефлексия", callback_data="Далее: Рефлексия")

    builder.adjust(1)
    
    return builder.as_markup()

def get_next_menu_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Меню", callback_data="Меню")

    builder.adjust(1)
    
    return builder.as_markup()

def get_menu_kb():
    builder = InlineKeyboardBuilder()

    # builder.button(text="Об обучении", callback_data="Об обучении")
    builder.button(text="Начать новое обучение", callback_data="Начать новое обучение")
    # builder.button(text="Поддержка", callback_data="Поддержка")
    # builder.button(text="Мои курсы", callback_data="Мои курсы")

    builder.adjust(1)
    
    return builder.as_markup()

def get_about_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Как правильно учиться", callback_data="Как правильно учиться")
    builder.button(text="Как работать с фреймворками", callback_data="Как работать с фреймворками")
    builder.button(text="Как применять знания на практике", callback_data="Как применять знания на практике")
    builder.button(text="Как проводить рефлексию", callback_data="Как проводить рефлексию")
    builder.button(text="Меню", callback_data="Меню")

    builder.adjust(1,1,1,1,1)
    
    return builder.as_markup()

def get_choice_course_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Продолжить", callback_data="Продолжить")
    builder.button(text="Выбрать", callback_data="Выбрать")


    builder.adjust(1,1)
    
    return builder.as_markup()

def get_this_lesson_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Да", callback_data="Да")
    builder.button(text="Меню", callback_data="Меню")


    builder.adjust(2)
    
    return builder.as_markup()

def get_reminder_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Начать", callback_data="Начать")

    builder.adjust(1)
    
    return builder.as_markup()

def get_next_menu_theme_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="Меню", callback_data="Меню")
    builder.button(text="Следующая тема", callback_data="Следующая тема")

    builder.adjust(1,1)
    
    return builder.as_markup()