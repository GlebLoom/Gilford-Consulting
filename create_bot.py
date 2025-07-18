### техника
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from decouple import AutoConfig
import json
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def load_users():
    try:
        with open('users.json', 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(list(users), f)
        
# Читаем .env
config = AutoConfig(search_path='.')
API_TOKEN = config('TOKEN')
print(f"DEBUG: ADMINS raw: {config('ADMINS')}")
ADMINS = [int(x.strip()) for x in config('ADMINS').split(',')]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Проверка: это админ?
def is_admin(user_id):
    print(f"DEBUG: user_id={user_id}, ADMINS={ADMINS}")
    return user_id in ADMINS
###









@dp.message(Command(commands=['reply']))
async def admin_reply(message: types.Message):
    
    if message.from_user.id not in ADMINS:
        return
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer('❌ Формат: /reply user_id текст')
        return 
    user_id = int(parts[1])
    text = parts[2]
    try:
        print(f"DEBUG chat.id={message.chat.id}, from_user.id={message.from_user.id}")
        await bot.send_message(user_id, text)
        await message.answer('✅ Отправлено.')
    except Exception as e:
        await message.answer(f'⚠️ Ошибка при отправке: {e}')







###
@dp.message()
async def catch_all_messages(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text.strip()
    if user_id not in ADMINS:
        response_map = {
            '/command1': 'Представительство в суде',
            '/command2': 'Взыскание задолженности',
            '/command3': 'Банкротство физических лиц',
            '/command4': 'Банкротство юридических лиц',
            '/command5': 'Защита интересов контролирующих должника лиц',
        }
        if message.text.strip() == '/start':
            if user_id not in USERS:
                USERS.add(user_id)
                save_users(USERS)
                for admin_id in ADMINS:
                    await bot.send_message(admin_id, f'🚀 Новый пользователь! User_id = {user_id}')
        elif user_text in response_map:
            description = response_map[user_text]
            await message.answer(f'Вы выбрали: {description}, мы скоро с вами свяжемся.')
            for admin_id in ADMINS:
                await bot.send_message(admin_id, f'👤 {user_id} : {description}')
        else:
            for admin_id in ADMINS:
                await bot.send_message(admin_id, f'👤 {user_id} : {user_text}')
###








         

###

async def main():
    global USERS
    USERS = load_users()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    


while True:
    asyncio.run(main())
###