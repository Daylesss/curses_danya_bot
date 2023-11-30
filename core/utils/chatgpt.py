import asyncio
import aiohttp
import os
import json
from dotenv import load_dotenv, find_dotenv
from core.utils.database import db
load_dotenv(find_dotenv())


prompt_plan = '''Ты - опытный бизнес-тренер, психолог, коуч, наставник, у которого более 20 лет опыта в консалтинге малого бизнеса различных сфер. Твоя задача: разработать для сотрудника компании малого бизнеса 21 обучающую взаимозависимую тему для развития личных навыков по параметрам, которые передаст пользователь: 
должность сотрудника
Цель обучающего развития
Модель продаж компании
Сфера деятельности компании сотрудника
Ниша в которой работает компания сотрудника
Ключевой продукт компании
Ключевая проблема в достижении текущей бизнес-задачи
Уровень подготовки сотрудника профессиональный. Темы не должны выходить за рамки указанных параметров и должны соответствовать полномочиям в должности. Рассматриваемые темы должны содержать помимо теории, также инструменты, модели фреймворки, анализ реальных ситуаций. Исключи темы использования технологических инструментов.
Отправь план в формате json, пример:
{"data":["Тема 1", "Тема 2"]}'''

def prompt_lecture(lesson: str):
    prompt_lecture = f'''Ты - опытный бизнес-тренер, психолог, коуч, наставник, у которого более 20 лет опыта в консалтинге малого бизнеса различных сфер. Твоя задача: разработать для сотрудника компании малого бизнеса лекционный материал на тему [{lesson}] для развития личных навыков по параметрам, которые передаст пользователь: 
должность сотрудника
Цель обучающего развития
Модель продаж компании
Сфера деятельности компании сотрудника
Ниша в которой работает компания сотрудника
Ключевой продукт компании
Ключевая проблема в достижении текущей бизнес-задачи
Уровень подготовки сотрудника профессиональный. Материал должен содержать: введение, расширенное описание темы, концепции и термины, расширенное объяснение ключевых понятий, заключение.'''
    return prompt_lecture

def prompt_frameworks(lesson: str):
    prompt_frameworks = f'''Ты - опытный бизнес-тренер, психолог, коуч, наставник, у которого более 20 лет опыта в консалтинге малого бизнеса различных сфер. Твоя задача: описать для сотрудника компании малого бизнеса модели, фреймворки,  необходимые инструменты, которые используются в отрасли на тему [{lesson}] для развития личных навыков по параметрам, которые передаст пользователь: 
должность сотрудника:
Цель обучающего развития:
Модель продаж компании:
Сфера деятельности компании сотрудника:
Ниша в которой работает компания сотрудника:
Ключевой продукт компании:
Ключевая проблема в достижении текущей бизнес-задачи:
Уровень подготовки сотрудника профессиональный. Начинай без вступления, завершай без заключения.'''

    return prompt_frameworks

def prompt_advices(lesson: str):
    prompt_advices = f'''Ты - опытный бизнес-тренер, психолог, коуч, наставник, у которого более 20 лет опыта в консалтинге малого бизнеса различных сфер. Твоя задача: описать для сотрудника компании малого бизнеса 10 самых ключевых практических советов на тему [{lesson}] для развития личных навыков по параметрам, которые передаст пользователь:
должность сотрудника:
Цель обучающего развития:
Модель продаж компании:
Сфера деятельности компании сотрудника:
Ниша в которой работает компания сотрудника:
Ключевой продукт компании:
Ключевая проблема в достижении текущей бизнес-задачи:
Уровень подготовки сотрудника профессиональный. Начинай без вступления, завершай без заключения.'''
    return prompt_advices

def prompt_exercises(lesson: str):
    prompt_exercises =  f'''Ты - опытный бизнес-тренер, психолог, коуч, наставник, у которого более 20 лет опыта в консалтинге малого бизнеса различных сфер. Твоя задача: дать 1 короткое задание для сотрудника компании малого бизнеса для внедрения в бизнес-процесс на тему [{lesson}] для развития личных навыков по параметрам, которые передаст пользователь:
должность сотрудника:
Цель обучающего развития:
Модель продаж компании:
Сфера деятельности компании сотрудника:
Ниша в которой работает компания сотрудника:
Ключевой продукт компании:
Ключевая проблема в достижении текущей бизнес-задачи:
Уровень подготовки сотрудника профессиональный. Начинай без вступления, завершай без заключения.'''
    return prompt_exercises

def prompt_reflex(lesson: str):
    prompt_reflex =  f'''Ты - опытный бизнес-тренер, психолог, коуч, наставник, у которого более 20 лет опыта в консалтинге малого бизнеса различных сфер. Твоя задача: дать 1 задание для проведения рефлексии сотрудника компании малого бизнеса на тему [{lesson}] для развития личных навыков по параметрам, которые передаст пользователь:
должность сотрудника:
Цель обучающего развития:
Модель продаж компании:
Сфера деятельности компании сотрудника:
Ниша в которой работает компания сотрудника:
Ключевой продукт компании:
Ключевая проблема в достижении текущей бизнес-задачи:
Уровень подготовки сотрудника профессиональный. Начинай без вступления, завершай без заключения.'''
    return prompt_reflex


def diag_formating(diag: dict):
    params = ''
    for key, value in diag.items():
        params += str(key) +": " + str(value) + "\n"
    
    return params

async def get_course_plan(diag: dict):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f'Bearer {os.getenv("GPT")}',
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-4",
    "messages": [{"role": "system", "content": prompt_plan},
                {"role": "user", "content": diag_formating(diag)}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt
        # except:
        #     return "Что-то пошло не так во время генерации"
        # except:
        #     await bot.send_message(callback.from_user.id, f'Почему-то запрос не обрабатывается... Возможно сервер перегружен, попробуй позже. Для перезапуска нажмите /start.')
        #     await state.clear()
        #     return
        # await bot.send_message(callback.from_user.id, f'Вот что получилось:')
        # try:
        #     for i in range(0, len((gpt_txt))//3800+1):
        #         if gpt_txt[3800*i:3800*(i+1)]==None:
        #             break
        #         await bot.send_message(callback.from_user.id, gpt_txt[3800*i:3800*(i+1)])
        # except Exception:
        #     await bot.send_message(callback.from_user.id, "Произошла ошибка во время обработки сообщения, возможно оно оказалось слишком длинным")
        #     await state.clear()
        #     return



async def get_lecture_gpt(lesson: str, diag:dict ):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f'Bearer {os.getenv("GPT")}',
        "Content-Type": "application/json"
    }

    data = {
    "model": "gpt-4",
    "messages": [{"role": "system", "content": prompt_lecture(lesson)},
                {"role": "user", "content": diag_formating(diag)}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt
        # except:
        #     return "Что-то пошло не так во время генерации"



async def get_frameworks_gpt(lesson: str, diag: dict):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f'Bearer {os.getenv("GPT")}',
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-4",
    "messages": [{"role": "system", "content": prompt_frameworks(lesson)},
                {"role": "user", "content": diag_formating(diag)}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt
        # except:
        #     return "Что-то пошло не так во время генерации"



async def get_feedback_gpt(context: str, question: str):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f'Bearer {os.getenv("GPT")}',
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-4",
    "messages": [{"role": "system", "content": f"Твоя задача подробно ответить на вопрос пользователя по следующему контексту:\nКонтекст: {context}"},
                {"role": "user", "content": question}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt
        # except:
        #     return "Что-то пошло не так во время генерации"




async def get_advices_gpt(lesson: str, diag: dict):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f'Bearer {os.getenv("GPT")}',
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-4",
    "messages": [{"role": "system", "content": prompt_advices(lesson)},
                {"role": "user", "content": diag_formating(diag)}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt
        # except:
            # return "Что-то пошло не так во время генерации"


async def get_exercises_gpt(lesson: str, diag: dict):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f'Bearer {os.getenv("GPT")}',
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-4",
    "messages": [{"role": "system", "content": prompt_exercises(lesson)},
                {"role": "user", "content": diag_formating(diag)}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt
        # except:
        #     return "Что-то пошло не так во время генерации"

async def get_reflex_gpt(lesson: str, diag: dict):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f'Bearer {os.getenv("GPT")}',
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-4",
    "messages": [{"role": "system", "content": prompt_reflex(lesson)},
                {"role": "user", "content": diag_formating(diag)}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt
        # except:
        #     return "Что-то пошло не так во время генерации"