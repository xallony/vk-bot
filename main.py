print("Бот работает")

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import json
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text

TOKEN = "vk1.a.MTYvYVpg7u4l-_TbYih_Ynxc24suuopPVg7j7JtZC9QfV_t4qxnF4zHHlRLWrfOkA53Vnlqzzx-21nR1jxg3OfB7W5m_PFtf7a07hF-dowWS-6DE-saCOiyrpNzJGLwn0euJSRu04yN-QNd_qiBQWjTnwTrauB0He1kHjmguCKGIR3nq93Bt27uA7CFjzIdfYMubm7BxYcccEPjco8z0Yw"
bot = Bot(token=TOKEN)

# база
def load_users():
    try:
        with open("users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

users = load_users()
change_name_mode = {}

# клавиатуры
start_kb = Keyboard(one_time=True).add(Text("Начать"))

menu_kb = Keyboard(one_time=False)
menu_kb.add(Text("Я")).row()
menu_kb.add(Text("Сменить ник"))

# если человек впервые пишет боту
@bot.on.message()
async def main(message: Message):
    user_id = str(message.from_id)
    text = message.text.strip()

    # если не зарегистрирован
    if user_id not in users:

        if text == "Начать":
            change_name_mode[user_id] = True
            await message.answer("Приветствую тебя! Придумай ник:")
        else:
            await message.answer(
                "Нажми кнопку «Начать» для регистрации",
                keyboard=start_kb
            )
        return

    # если меняет ник
    if change_name_mode.get(user_id):
        users[user_id] = text
        save_users(users)
        change_name_mode[user_id] = False
        await message.answer(
            f"твой новый ник - {text}",
            keyboard=menu_kb
        )
        return

    # обычное меню
    if text == "Сменить ник":
        change_name_mode[user_id] = True
        await message.answer("Напиши новый ник:")
        return

    if text == "Я":
        await message.answer(
            f"Приветствую тебя {users[user_id]}, на твоем балансе 0₽",
            keyboard=menu_kb
        )
        return

    await message.answer(
        f"Я не понимаю тебя",
        keyboard=menu_kb
    )

print("Бот запущен, жду сообщения...")
bot.run_forever()