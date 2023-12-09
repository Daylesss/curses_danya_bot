import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
import datetime

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
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: !!!!!!!!!!!!!!!!!!! БАЗА ДАНЫЫХ ЗАКРЫЛАСЬ \n")
    
    def user_exists(self, tg_id):
        try:
            self.cursor.execute("SELECT user_id FROM users WHERE tg_id = (%s)", (tg_id,))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: user_exists --{exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        return bool(self.cursor.fetchall())
    
    def get_user_id(self, tg_id):
        try:
            self.cursor.execute("SELECT user_id FROM users WHERE tg_id = (%s)", (tg_id,))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_user_id --{exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        try:
            ret = self.cursor.fetchone()[0]
            return ret
        except:
            return None
    
    def get_tg_id(self, user_id):
        try:
            self.cursor.execute("SELECT tg_id FROM users WHERE user_id = (%s)", (user_id,))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_tg_id -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        try:
            ret = self.cursor.fetchone()[0]
            return ret
        except:
            return None
    
    
    def add_user(self, tg_id):
        try:
            self.cursor.execute("INSERT INTO users (tg_id) VALUES (%s)", (tg_id,))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: add_user -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
    
    def insert_plan(self, user_id, diagnostics, plan):
        try:
            data = json.dumps(diagnostics)
        except:
            data = dict()
        try:
            self.cursor.execute("INSERT INTO plans (user_id, diagnostic, plan) VALUES (%s, %s, %s)", (user_id, data, plan))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: insert_plan -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
    
    def get_diag(self, course_id: int)->dict | None:
        try:
            self.cursor.execute("SELECT plan_id FROM user_courses WHERE course_id = (%s)", (course_id,))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_diag -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        plan_id = self.cursor.fetchone()
        try:
            self.cursor.execute("SELECT diagnostic FROM plans WHERE plan_id = %s", (plan_id, ))
            return json.loads(self.cursor.fetchone()[0])
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_diag --{exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        except Exception as ex:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: {ex} \n")
            return None

    def get_plan_id(self, user_id):
        try:
            self.cursor.execute("SELECT plan_id FROM plans WHERE user_id = %s AND plan_created = (SELECT MAX(plan_created) FROM plans WHERE user_id = %s)", (user_id, user_id))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_plan_id {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        try:
            ret = self.cursor.fetchone()[0]
            return ret
        except:
            return None
    
    def get_plan(self, plan_id):
        try:
            self.cursor.execute("SELECT plan FROM plans WHERE plan_id = %s", (plan_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_plan {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        try:
            ret = self.cursor.fetchone()[0]
            return ret
        except:
            return None
    
    def set_course(self, plan_id: int):
        try:
            self.cursor.execute("SELECT user_id FROM plans WHERE plan_id = %s", (plan_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: set_course -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        user_id = self.cursor.fetchone()
        if user_id:
            try:
                self.cursor.execute("INSERT INTO user_courses (user_id, plan_id) VALUES (%s, %s)", (user_id[0], plan_id))
                self.cursor.execute("SELECT course_id FROM user_courses WHERE user_id = %s AND course_created = (SELECT MAX(course_created) FROM user_courses WHERE user_id = %s)", (user_id[0], user_id[0]))
                course_id = self.cursor.fetchone()[0]
                self.cursor.execute("UPDATE users SET latest_course_id = %s WHERE user_id = %s", (course_id, user_id[0]))
            except psycopg2.ProgrammingError as exc:
                with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                    time =datetime.datetime.utcnow()
                    f.write(f"{time}: set_course -- {exc.message} \n")
                self.connection.rollback()
            except psycopg2.InterfaceError as exc:
                with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                    time =datetime.datetime.utcnow()
                    f.write(f"{time}: что-то с подключением -- {exc.message} \n")
                self.connection = psycopg2.connect(user="postgres",
                                            # пароль, который указали при установке PostgreSQL
                                            password="4587",
                                            host="127.0.0.1",
                                            port="5432",
                                            database = 'postgres')
                self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                # Курсор для выполнения операций с базой данных
                self.cursor = self.connection.cursor()
            
        else:
            return None

    def upd_latest_course(self, tg_id: int, course_id: int):
        try:
            self.cursor.execute("UPDATE users SET latest_course_id = %s WHERE tg_id = %s", (course_id, tg_id))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: upd_latest_course -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
    
    def get_latest_course(self, user_id: int):
        try:
            self.cursor.execute("SELECT latest_course_id FROM users WHERE user_id = %s", (user_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_latest_course -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        try: 
            return self.cursor.fetchone()[0]
        except: return None
        

    def get_day(self, tg_id :int):
        try:
            self.cursor.execute("SELECT latest_course_id FROM users WHERE tg_id = %s", (tg_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_day -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        course = self.cursor.fetchone()
        if course:
            try:
                self.cursor.execute("SELECT day FROM user_courses WHERE course_id = %s", (course,))
            except psycopg2.ProgrammingError as exc:
                with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                    time =datetime.datetime.utcnow()
                    f.write(f"{time}: get_day2 --  {exc.message} \n")
                self.connection.rollback()
            except psycopg2.InterfaceError as exc:
                with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                    time =datetime.datetime.utcnow()
                    f.write(f"{time}: что-то с подключением -- {exc.message} \n")
                self.connection = psycopg2.connect(user="postgres",
                                            # пароль, который указали при установке PostgreSQL
                                            password="4587",
                                            host="127.0.0.1",
                                            port="5432",
                                            database = 'postgres')
                self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                # Курсор для выполнения операций с базой данных
                self.cursor = self.connection.cursor()
            return self.cursor.fetchone()[0]
        
    def get_day_status(self, tg_id :int):
        try:
            self.cursor.execute("SELECT latest_course_id FROM users WHERE tg_id = %s", (tg_id, ))
            course = self.cursor.fetchone()
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_day_status -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        if course:
            try:
                self.cursor.execute("SELECT day_status FROM user_courses WHERE course_id = %s", (course,))
            except psycopg2.ProgrammingError as exc:
                with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                    time =datetime.datetime.utcnow()
                    f.write(f"{time}: get_day_status(2) -- {exc.message} \n")
                self.connection.rollback()
            except psycopg2.InterfaceError as exc:
                with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                    time =datetime.datetime.utcnow()
                    f.write(f"{time}: что-то с подключением -- {exc.message} \n")
                self.connection = psycopg2.connect(user="postgres",
                                            # пароль, который указали при установке PostgreSQL
                                            password="4587",
                                            host="127.0.0.1",
                                            port="5432",
                                            database = 'postgres')
                self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                # Курсор для выполнения операций с базой данных
                self.cursor = self.connection.cursor()
            return self.cursor.fetchone()[0]
    
    def get_day_status2(self, user_id :int):
        try:
            self.cursor.execute("SELECT latest_course_id FROM users WHERE user_id = %s", (user_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_day_status2 -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        course = self.cursor.fetchone()
        if course:
            try:
                self.cursor.execute("SELECT day_status FROM user_courses WHERE course_id = %s", (course,))
            except psycopg2.ProgrammingError as exc:
                with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                    time =datetime.datetime.utcnow()
                    f.write(f"{time}:get_day_status2(2) -- {exc.message} \n")
                self.connection.rollback()
            except psycopg2.InterfaceError as exc:
                with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                    time =datetime.datetime.utcnow()
                    f.write(f"{time}: что-то с подключением -- {exc.message} \n")
                self.connection = psycopg2.connect(user="postgres",
                                            # пароль, который указали при установке PostgreSQL
                                            password="4587",
                                            host="127.0.0.1",
                                            port="5432",
                                            database = 'postgres')
                self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                # Курсор для выполнения операций с базой данных
                self.cursor = self.connection.cursor()
            return self.cursor.fetchone()[0]

    def update_day_status(self, course_id, status: str):
        try:
            self.cursor.execute("UPDATE user_courses SET day_status = %s WHERE course_id = %s", (status, course_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: update_day_status -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
    
    def update_day(self, course_id, day):
        try:
            self.cursor.execute("UPDATE user_courses SET day = %s WHERE course_id = %s", (day, course_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: update_day -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
    
    def update_course_status(self, course_id, status):
        try:
            self.cursor.execute("UPDATE user_courses SET course_status = %s WHERE course_id = %s", (status, course_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: update_course_status -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
    
    def get_user_courses(self, user_id):
        try:
            self.cursor.execute("SELECT course_created, course_status, course_id FROM user_courses WHERE user_id = %s ORDER BY course_created", (user_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_user_courses -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        return self.cursor.fetchall()
    

    def get_course_status(self, course_id):
        try:
            self.cursor.execute("SELECT course_status FROM user_courses WHERE course_id = %s", (course_id, ))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_course_status -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        try:
            return self.cursor.fetchone()[0]
        except: return None

    def check_table(self, name_table):
        try:
            self.cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name= %s)", (name_table,))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: check_table -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        return bool(self.cursor.fetchone()[0])

    def create_sender_table(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (user_id bigint NOT NULL, statuse text, description text, PRIMARY KEY (user_id)) WITH ( OIDS = FALSE)")
            self.cursor.execute(f"INSERT into {table_name} (user_id, statuse, description) SELECT user_id, 'waiting', NULL FROM users")
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: create_sender_table --  {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()

    def delete_sender_table(self, name_comp):
        try:
            self.cursor.execute(f'DROP TABLE IF EXISTS {name_comp}')
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: delete_sender_table -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
    
    def update_statuse(self, table_name, user_id, statuse, description):
        try:
            self.cursor.execute(f"UPDATE {table_name} SET statuse=%s, description = %s WHERE user_id= %s", (statuse, description, user_id))
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: update_statuse -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        # query= f"UPDATE {table_name} SET statuse='{statuse}', description ='{description}' WHERE user_id={user_id}"
    
    def get_users(self, table_name):
        try:
            self.cursor.execute(f"SELECT user_id FROM {table_name} WHERE statuse='waiting'")
        except psycopg2.ProgrammingError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: get_users -- {exc.message} \n")
            self.connection.rollback()
        except psycopg2.InterfaceError as exc:
            with open("BD_Logs.txt", "a", encoding = "utf-8") as f:
                time =datetime.datetime.utcnow()
                f.write(f"{time}: что-то с подключением -- {exc.message} \n")
            self.connection = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL
                                        password="4587",
                                        host="127.0.0.1",
                                        port="5432",
                                        database = 'postgres')
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # Курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()
        result = self.cursor.fetchall()

        return [user[0] for user in result]

db = MonoqleDB()

def is_subscribed(user_id: int):
    return user_id
