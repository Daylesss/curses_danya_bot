import asyncio
import aiohttp
import json

prompt = "Ты - опытный бизнес-тренер, психолог, коуч, наставник, у которого более 20 лет опыта в консалтинге малого бизнеса различных сфер. Твоя задача: разработать для сотрудника компании малого бизнеса 21 обучающую взаимозависимую тему для развития личных навыков по параметрам: должность сотрудника: [менеджер по продажам]. Цель обучающего развития: [увеличить продажи].  Модель продаж компании: [B2B2C]. Сфера деятельности компании сотрудника: [торговля]. Ниша в которой работает компания сотрудника: [бьюти индустрия]. Ключевой продукт компании [косметика]. Ключевая проблема в достижении текущей бизнес-задачи [низкие продажи]. Уровень подготовки сотрудника профессиональный. Темы не должны выходить за рамки указанных параметров и должны соответствовать полномочиям в должности. Рассматриваемые темы должны содержать помимо теории, также инструменты, модели фреймворки, анализ реальных ситуаций. Исключи темы использования технологических инструментов."

def get_diag_params():
    return 0

async def get_course_plan(id: int):
    params = get_diag_params()
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-3.5-turbo-16k",
    "messages": [{"role": "system", "content": "ТЫ добрый советчик"},
                {"role": "user", "content": "Как дела"}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt
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



async def get_lecture_gpt(id: int):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-3.5-turbo-16k",
    "messages": [{"role": "system", "content": "Продублируй слова, которые введет пользователь"},
                {"role": "user", "content": "Про курсы"}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt



async def get_frameworks_gpt(id: int):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-3.5-turbo-16k",
    "messages": [{"role": "system", "content": "Продублируй слова, которые введет пользователь"},
                {"role": "user", "content": "фреймворк"}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt



async def get_feedback_gpt(context: str, question: str):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-3.5-turbo-16k",
    "messages": [{"role": "system", "content": "Продублируй слова, которые введет пользователь"},
                {"role": "user", "content": question}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt




async def get_advices_gpt(id: int):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-3.5-turbo-16k",
    "messages": [{"role": "system", "content": "Продублируй слова, которые введет пользователь"},
                {"role": "user", "content": "советы"}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt


async def get_exercises_gpt(id: int):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-3.5-turbo-16k",
    "messages": [{"role": "system", "content": "Продублируй слова, которые введет пользователь"},
                {"role": "user", "content": "Задания"}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt

async def get_reflex_gpt(id: int):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
    "model": "gpt-3.5-turbo-16k",
    "messages": [{"role": "system", "content": "Продублируй слова, которые введет пользователь"},
                {"role": "user", "content": "рефлексия"}],
    "temperature": 0.7}

    timeout = aiohttp.ClientTimeout(total=600)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # try:
            resp= await session.post(url, headers=headers, data=json.dumps(data))
            
            gpt_resp = await resp.json()
            
            gpt_txt = gpt_resp["choices"][0]["message"]["content"]
            return gpt_txt