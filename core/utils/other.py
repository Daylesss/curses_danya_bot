from core.utils.database import db

def get_courses_message(user_id):
    courses = db.get_user_courses(user_id)
    course_dict = {}
    for course in enumerate(courses):
        course_str = f"{course[0] + 1}) [{course[1][0]}] - status [{course[1][1]}]\n"
        num = course[0] + 1
        course_dict[num] = (course[1][2], course_str)
    
    return course_dict