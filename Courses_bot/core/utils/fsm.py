from aiogram.fsm.state import StatesGroup, State

class DiagFSM(StatesGroup):
    POSITION = State()
    MODEL = State()
    FIELD = State() 
    NICHE = State()
    SERVICE = State()
    GOAL = State()
    PROBLEM = State()
    END_DIAG = State()
    RESET = State()


class CourseFSM(StatesGroup):
    PLAN = State() 
    COURSE = State()
    LECTURE = State()
    FEEDBACK_LECTURE = State()
    BEFORE_FRAMEWORKS = State()
    FRAMEWORKS = State()
    FEEDBACK_FRAMEWORKS = State()
    BEFORE_ADVICES = State()
    ADVICES = State()
    EXERCISES = State()
    REFLEX = State()


class BaseFSM(StatesGroup):
    MENU = State()
    ABOUT = State()
    NEW =State()
    SUPPORT = State()