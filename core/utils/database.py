import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json


class MonoqleDB:
    def __init__(self):
        try:
            # Подключение к существующей базе данных
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            self.cursor.close()
            self.connection.close()
            print("Соединение с PostgreSQL закрыто")
    
    def user_exists(self, tg_id):
        self.cursor.execute("SELECT user_id FROM users WHERE tg_id = (%s)", (tg_id,))
        return bool(self.cursor.fetchall())
    
    def get_user_id(self, tg_id):
        self.cursor.execute("SELECT user_id FROM users WHERE tg_id = (%s)", (tg_id,))
        try:
            ret = self.cursor.fetchone()[0]
            return ret
        except:
            return None
    
    def get_tg_id(self, user_id):
        self.cursor.execute("SELECT tg_id FROM users WHERE user_id = (%s)", (user_id,))
        try:
            ret = self.cursor.fetchone()[0]
            return ret
        except:
            return None
    
    
    def add_user(self, tg_id):
        self.cursor.execute("INSERT INTO users (tg_id) VALUES (%s)", (tg_id,))
    
    def insert_plan(self, user_id, diagnostics, plan):
        data = json.dumps(diagnostics)
        self.cursor.execute("INSERT INTO plans (user_id, diagnostic, plan) VALUES (%s, %s, %s)", (user_id, data, plan))
    
    def get_diag(self, course_id: int)->dict | None:
        self.cursor.execute("SELECT plan_id FROM user_courses WHERE course_id = (%s)", (course_id,))
        plan_id = self.cursor.fetchone()
        try:
            self.cursor.execute("SELECT diagnostic FROM plans WHERE plan_id = %s", (plan_id, ))
            return json.loads(self.cursor.fetchone()[0])
        except:
            return None

    def get_plan_id(self, user_id):
        self.cursor.execute("SELECT plan_id FROM plans WHERE user_id = %s AND plan_created = (SELECT MAX(plan_created) FROM plans WHERE user_id = %s)", (user_id, user_id))
        try:
            ret = self.cursor.fetchone()[0]
            return ret
        except:
            return None
    
    def get_plan(self, plan_id):
        self.cursor.execute("SELECT plan FROM plans WHERE plan_id = %s", (plan_id, ))
        try:
            ret = self.cursor.fetchone()[0]
            return ret
        except:
            return None
    
    def set_course(self, plan_id: int):
        self.cursor.execute("SELECT user_id FROM plans WHERE plan_id = %s", (plan_id, ))
        user_id = self.cursor.fetchone()
        if user_id:
            self.cursor.execute("INSERT INTO user_courses (user_id, plan_id) VALUES (%s, %s)", (user_id[0], plan_id))
            self.cursor.execute("SELECT course_id FROM user_courses WHERE user_id = %s AND course_created = (SELECT MAX(course_created) FROM user_courses WHERE user_id = %s)", (user_id[0], user_id[0]))
            course_id = self.cursor.fetchone()[0]
            self.cursor.execute("UPDATE users SET latest_course_id = %s WHERE user_id = %s", (course_id, user_id[0]))
            
        else:
            return None

    def upd_latest_course(self, tg_id: int, course_id: int):
        self.cursor.execute("UPDATE users SET latest_course_id = %s WHERE tg_id = %s", (course_id, tg_id))
    
    def get_latest_course(self, user_id: int):
        self.cursor.execute("SELECT latest_course_id FROM users WHERE user_id = %s", (user_id, ))
        try: 
            return self.cursor.fetchone()[0]
        except: return None
        

    def get_day(self, tg_id :int):
        self.cursor.execute("SELECT latest_course_id FROM users WHERE tg_id = %s", (tg_id, ))
        course = self.cursor.fetchone()
        if course:
            self.cursor.execute("SELECT day FROM user_courses WHERE course_id = %s", (course,))
            return self.cursor.fetchone()[0]
        
    def get_day_status(self, tg_id :int):
        self.cursor.execute("SELECT latest_course_id FROM users WHERE tg_id = %s", (tg_id, ))
        course = self.cursor.fetchone()
        if course:
            self.cursor.execute("SELECT day_status FROM user_courses WHERE course_id = %s", (course,))
            return self.cursor.fetchone()[0]
    
    def get_day_status2(self, user_id :int):
        self.cursor.execute("SELECT latest_course_id FROM users WHERE user_id = %s", (user_id, ))
        course = self.cursor.fetchone()
        if course:
            self.cursor.execute("SELECT day_status FROM user_courses WHERE course_id = %s", (course,))
            return self.cursor.fetchone()[0]

    def update_day_status(self, course_id, status: str):
        self.cursor.execute("UPDATE user_courses SET day_status = %s WHERE course_id = %s", (status, course_id, ))
    
    def update_day(self, course_id, day):
        self.cursor.execute("UPDATE user_courses SET day = %s WHERE course_id = %s", (day, course_id, ))
    
    def update_course_status(self, course_id, status):
        self.cursor.execute("UPDATE user_courses SET course_status = %s WHERE course_id = %s", (status, course_id, ))
    
    def get_user_courses(self, user_id):
        self.cursor.execute("SELECT course_created, course_status, course_id FROM user_courses WHERE user_id = %s ORDER BY course_created", (user_id, ))
        return self.cursor.fetchall()
    def get_course_status(self, course_id):
        self.cursor.execute("SELECT course_status FROM user_courses WHERE course_id = %s", (course_id, ))
        try:
            return self.cursor.fetchone()[0]
        except: return None

    def check_table(self, name_table):
        self.cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name= %s)", (name_table,))
        return bool(self.cursor.fetchone()[0])

    def create_sender_table(self, table_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (user_id bigint NOT NULL, statuse text, description text, PRIMARY KEY (user_id)) WITH ( OIDS = FALSE)")
        self.cursor.execute(f"INSERT into {table_name} (user_id, statuse, description) SELECT user_id, 'waiting', NULL FROM users")

    def delete_sender_table(self, name_comp):
        self.cursor.execute(f'DROP TABLE IF EXISTS {name_comp}')
    
    def update_statuse(self, table_name, user_id, statuse, description):
        self.cursor.execute(f"UPDATE {table_name} SET statuse=%s, description = %s WHERE user_id= %s", (statuse, description, user_id))
        # query= f"UPDATE {table_name} SET statuse='{statuse}', description ='{description}' WHERE user_id={user_id}"
    
    def get_users(self, table_name):
        self.cursor.execute(f"SELECT user_id FROM {table_name} WHERE statuse='waiting'")
        result = self.cursor.fetchall()

        return [user[0] for user in result]

db = MonoqleDB()

def is_subscribed(user_id: int):
    return user_id
