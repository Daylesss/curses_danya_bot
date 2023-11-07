
def insert_diag(data: dict):
    print("УСПЕШНО ВСТАВЛЕН")
    print(*data)
    


def save_plan(plan: str) -> None:
    print("saved")
    

def on_course() -> None:
    print("on course")
    
def get_cur_course(user_id: int):
    print("Find id of curr course")

def get_lesson(user_id:int):
    get_cur_course(user_id=user_id)
    print("DAY THEME")
    
    return 0
    

def get_last_bot_message():
    print("LAST BOT MESSAGE")
    return 1

def is_subscribed(user_id: int):
    return user_id
