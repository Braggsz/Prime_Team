import telebot
from telebot import types
import time
import random
import sqlite3
import schedule
import threading
from datetime import datetime

TOKEN = '7039961825:AAGmyb-lFESj2INpi81JWQAV9kgZwPBtJSU'
bot = telebot.TeleBot(TOKEN)

# Список ID админов
ADMINS = [6821884320]  # Укажи тут ID админов


# Функция для отправки сообщений всем пользователям
def send_message_to_all_users(message):
    cursor.execute('SELECT chat_id FROM users')
    users = cursor.fetchall()
    for user in users:
        bot.send_message(user[0], message)

# Функция для отправки FULL WORK!
def send_full_work():
    send_message_to_all_users("✅ FULL WORK ✅")

# Функция для отправки STOP WORK!
def send_stop_work():
    send_message_to_all_users("❌ STOP WORK ❌")

# Запланируем задачи
schedule.every().day.at("05:00").do(send_full_work)
schedule.every().day.at("00:00").do(send_stop_work)

# Функция для запуска планировщика в отдельном потоке
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запускаем планировщик в отдельном потоке
threading.Thread(target=run_schedule, daemon=True).start()

def get_work_status():
    current_time = datetime.now().time()
    print(f"Текущее время: {current_time}")  # Добавь этот вывод для отладки
    if current_time >= datetime.strptime("05:00", "%H:%M").time() and current_time <= datetime.strptime("23:59", "%H:%M").time():
        return "✅ FULL WORK ✅"
    else:
        return "❌ STOP WORK ❌"



submitted_message_id = None


def reset_users():
    cursor.execute('DELETE FROM users')  # Удаляет всех пользователей из таблицы
    conn.commit()




# Функция для безопасного удаления сообщения
def safe_delete_message(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Не удалось удалить сообщение {message_id} в чате {chat_id}: {e}")




@bot.message_handler(content_types=['photo', 'video', 'audio', 'document', 'voice', 'animation', 'video_note', 'sticker'])
def get_photo(message):
    msg = bot.reply_to(message, '''<u><b><i>К сожалению, мы не обрабатываем такие файлы. 📂

Пожалуйста, используйте только текстовые команды или кнопки для взаимодействия. Спасибо за понимание!</i></b></u>''', parse_mode='html', reply_markup=create_main_menu())




# Подключение к базе данных SQLite
conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()

def create_database():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Создаем таблицу users, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            country TEXT,
            user_hash TEXT,
            referral_link TEXT,
            is_registered INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

# Запускаем создание базы данных
create_database()

# Функция генерации хэша
def generate_hash():
    return "#WLR" + str(random.randint(100000, 999999))

# Функция генерации реферальной ссылки
def generate_referral_link(chat_id):
    return f"https://braggsz.github.io/Cinema/?ref={chat_id}"


# Функция для сохранения данных пользователя в базу данных
def save_user_data(chat_id, name, age, country, user_hash, referral_link=None, is_registered=0):
    cursor.execute('''INSERT OR REPLACE INTO users (chat_id, name, age, country, user_hash, referral_link, is_registered)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (chat_id, name, age, country, user_hash, referral_link, is_registered))
    conn.commit()


# Функция для получения данных пользователя из базы данных
def get_user_data(chat_id):
    cursor.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,))
    return cursor.fetchone()

# Стартовое сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_info = get_user_data(chat_id)

    # Проверяем, зарегистрирован ли пользователь
    if user_info and user_info[5] == 1:
        # Пользователь уже зарегистрирован — показываем его профиль
        show_profile(chat_id)
    else:
        # Если не зарегистрирован, запускаем процесс регистрации
        bot.send_message(chat_id, """Приветствуем в команде <b>Prime Team!</b> 👋""", parse_mode='HTML')
        bot.send_message(chat_id, '''<b>⚠️ Ответ не обязателен! ⚠️</b>
                         
 <b>1️⃣ Как Вас зовут?</b>   
                                               
<i>Для пропуска этого вопроса отправьте текст: " <code>Hoin.</code> "</i> ''', parse_mode='HTML')
        bot.register_next_step_handler(message, ask_name )

# Сохранение имени
def ask_name(message):
    chat_id = message.chat.id
    name = message.text
    save_user_data(chat_id, name, None, None, None)
    bot.send_message(chat_id, '''<b>⚠️ Ответ не обязателен! ⚠️</b>
                         
 <b>2️⃣ Сколько Вам лет?</b>   
                                               
<i>Для пропуска этого вопроса отправьте текст: " <code>Hoin.</code> "</i> ''', parse_mode='HTML')
    bot.register_next_step_handler(message, ask_age)

# Сохранение возраста
def ask_age(message):
    chat_id = message.chat.id
    age = message.text
    cursor.execute('UPDATE users SET age = ? WHERE chat_id = ?', (age, chat_id))
    conn.commit()
    bot.send_message(chat_id, '''<b>⚠️ Ответ не обязателен! ⚠️</b>
                         
 <b>3️⃣ В какой стране Вы проживаете?</b>   
                                               
<i>Для пропуска этого вопроса отправьте текст: " <code>Hoin.</code> "</i> ''' , parse_mode='HTML')
    bot.register_next_step_handler(message, ask_country)

# Сохранение страны и генерация хэша
def ask_country(message):
    chat_id = message.chat.id
    country = message.text
    user_hash = generate_hash()
    referral_link = generate_referral_link(chat_id)  # Генерируем реферальную ссылку
    cursor.execute('UPDATE users SET country = ?, user_hash = ?, referral_link = ? WHERE chat_id = ?', 
                   (country, user_hash, referral_link, chat_id))
    conn.commit()
    bot.send_message(chat_id, '''<b>💬 Расскажите нам о себе:</b>

 
<b>◉ Где Вы работали? 🏢</b>
<b>◉ Как долго? ⏳</b>
<b>◉ Какой Ваш план работы? 📋</b>

 
🔺🔻 <b>Обратите внимание:</b> Ответ на этот вопрос <u>обязателен</u>! Пожалуйста, напишите <b>кратко и понятно, без ошибок.</b> В противном случае ваша заявка не будет рассмотрена. 🔻🔺''', parse_mode='HTML')
    bot.register_next_step_handler(message, show_summary)


# Отображение данных пользователя и отправка фото
def show_summary(message):
    chat_id = message.chat.id
    user_info = get_user_data(chat_id)
    user_id = message.from_user.id

    # Сообщение с данными пользователя
    summary_text = f'''<b>✨ Ваша заявка готова к отправке! ✨</b>

Если вам нужно что-то исправить, <b>нажмите команду /start и пройдите всё с самого начала. 🔄</b>

 
<b>👉 Для отправки заявки нажмите кнопку ниже: 👇</b>'''

    # Отправляем данные пользователя и кнопку для отправки заявки
    markup = types.InlineKeyboardMarkup()
    submit_button = types.InlineKeyboardButton(text="✉️ Отправить заявку на рассмотрение 🚀", callback_data="submit_application")
    markup.add(submit_button)

    bot.send_message(chat_id, summary_text, reply_markup=markup , parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "submit_application")
def process_application(call):
    global submitted_message_id  # Используем глобальную переменную
    chat_id = call.message.chat.id
    
    # Сохраняем ID сообщения о готовности заявки
    ready_message_id = call.message.message_id
    
    submitted_message = bot.send_message(chat_id, """<b><i>✅ Ваша заявка успешно отправлена! 🎉
    Ожидайте <b>.</b> . <i>.</i></i></b>""" , parse_mode='HTML')
    
    submitted_message_id = submitted_message.message_id  # Сохраняем ID сообщения

    # Удаляем сообщение о готовности заявки
    safe_delete_message(chat_id, ready_message_id)  # Удаляем сообщение о готовности
    
    # Отправляем сообщение через 2 секунды
    time.sleep(2)
    bot.send_message(chat_id, "<b>✅ Администратор успешно принял вашу заявку ✅</b>", parse_mode='HTML')

    # Удаляем сообщение с подтверждением отправки заявки
    safe_delete_message(chat_id, submitted_message_id)  # Удаляем сообщение

    # Устанавливаем статус "зарегистрирован"
    cursor.execute('UPDATE users SET is_registered = 1 WHERE chat_id = ?', (chat_id,))
    conn.commit()

    # Показать профиль и статус
    show_profile(chat_id)

    # Отправить основное меню


    




# Обработка нажатия на кнопку "Мой профиль 👤"
@bot.message_handler(func=lambda message: message.text == "Мой профиль 👤")
def profile_handler(message):
    chat_id = message.chat.id
    show_profile(chat_id)

def show_profile(chat_id):
    user_id = chat_id
    user_info = get_user_data(chat_id)
    name = user_info[1] if user_info[1] else 'Не указано'
    age = user_info[2] if user_info[2] else 'Не указано'
    country = user_info[3] if user_info[3] else 'Не указано'
    user_hash = user_info[4] if user_info[4] else 'Не сгенерирован'

    # Проверка на админа
    if user_id in ADMINS:
        status = "ADMIN"
    else:
        status = "Воркер"

    profile_text = f"""<b>🌟 ꧁❂༺ Ваш профиль ༻❂꧂ 🌟</b>

<b>🆔 Ваш ID:</b> <code>{user_id}</code>

───────────────────────────

<b>🏗 Количество рефералов:</b> <code>0</code>
<b>🌟 Ваш ранк:</b> <code>0.01</code>
<b>🛡 Ваш хэш:</b> {user_hash}
<b>⚖️ Статус:</b> <i><code>{status}</code></i>
"""

    # Получаем текущее сообщение (FULL WORK или STOP WORK)
    work_status = get_work_status()
    print(f"Статус работы: {work_status}")  # Добавь этот вывод для отладки

    # Путь к фото (замени на реальный путь к фото)
    photo_path = "img/131c549c-85bf-4641-b4c6-1295fb4af0f8.jpg"

    # Отправка фото с текстом
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id, photo, caption=profile_text, reply_markup=create_main_menu(), parse_mode='HTML')
    
    # Отправляем статус работы в отдельном сообщении
    bot.send_message(chat_id, f"<b>{work_status}</b>", parse_mode='HTML')


# Функция для создания основного меню
def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton("Мой профиль 👤")
    btn2 = types.KeyboardButton("Чаты 💬")
    btn3 = types.KeyboardButton("🔗Создать ссылку")
    btn4 = types.KeyboardButton("Мануалы 📚")

    
    markup.add(btn1)
    markup.add(btn3)
    markup.add(btn2, btn4)
    return markup

@bot.message_handler(commands=['reset_users'])
def reset_users_command(message):
    chat_id = message.chat.id
    if chat_id in ADMINS:  # Проверяем, является ли пользователь администратором
        reset_users()
        bot.send_message(chat_id, "<b><u>✅ Все пользователи успешно аннулированы! 🔄</u></b>", parse_mode='HTML')
    else:
        bot.send_message(chat_id, "<b><u>❌ У вас нет прав для выполнения этой команды! 🔒</u></b>", parse_mode='HTML')

# Обработка нажатия на кнопку "Мой профиль 👤"
@bot.message_handler(func=lambda message: message.text == "Мой профиль 👤")
def profile_handler(message):
    chat_id = message.chat.id
    show_profile(chat_id)
    

# Обработка нажатия на кнопку "Чаты 💬"
@bot.message_handler(func=lambda message: message.text == "Чаты 💬")
def chats_handler(message):
    chat_id = message.chat.id

    # Текст для чатов
    chat_text = "<b>🔗 Вот ссылки для чатов: 💬</b>\n"

    # Создаем inline-кнопки с ссылками на чаты
    markup = types.InlineKeyboardMarkup()
    
    chat1_button = types.InlineKeyboardButton(text=" 💬 Чат", url="https://t.me/+RSSW4Dhcges3YTUx")
    chat2_button = types.InlineKeyboardButton(text="💸 Выплаты", url="https://t.me/+RSSW4Dhcges3YTUx")
    
    markup.add(chat1_button, chat2_button)

    bot.send_message(chat_id, chat_text, reply_markup=markup, parse_mode='HTML')


    

# Обработка нажатия на кнопку "🔗Создать ссылку"
@bot.message_handler(func=lambda message: message.text == "<b>🔗Создать ссылку</b>")
def create_promo_code_handler(message):
    chat_id = message.chat.id
    user_info = get_user_data(chat_id)
    referral_link = user_info[6]  # Получаем реферальную ссылку
    bot.send_message(chat_id, f"<b><u>🌟 Вот ваша реферальная ссылка:<code>{referral_link}</code></u></b>", parse_mode='HTML')


# Обработка нажатия на кнопку "Мануалы 📚"
@bot.message_handler(func=lambda message: message.text == "Мануалы 📚")
def chats_handler(message):
    chat_id = message.chat.id

    # Текст для чатов
    chat_text = "<b>📚 Вот канал с мануалами:\n</b>"

    # Создаем inline-кнопки с ссылками на чаты
    markup = types.InlineKeyboardMarkup()
    
    chat1_button = types.InlineKeyboardButton(text="📖 Мануал", url="https://t.me/+OBWZtY7qCFdmNjNh")
    markup.add(chat1_button)

    bot.send_message(chat_id, chat_text, reply_markup=markup, parse_mode='HTML')

# Обработка нажатия на кнопку "👩‍🏫Наставники"
@bot.message_handler(func=lambda message: message.text == "👩‍🏫Наставники")
def chats_handler(message):
    chat_id = message.chat.id

    # Текст для чатов
    chat_text = "<b>🌟 Выбери себе своего наставника:</b>\n"

    # Создаем inline-кнопки с ссылками на чаты
    markup = types.InlineKeyboardMarkup()
    
    chat1_button = types.InlineKeyboardButton(text=" Дмитрий", url="https://t.me/Dimchik2006")
    chat2_button = types.InlineKeyboardButton(text="Даниил", url="https://t.me/qalfooe")
    
    markup.add(chat1_button)
    markup.add(chat2_button)

    bot.send_message(chat_id, chat_text, reply_markup=markup, parse_mode='HTML')

# Запускаем бота
bot.polling(none_stop=True)