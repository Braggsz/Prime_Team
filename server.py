from flask import Flask, request, redirect
import sqlite3
import telebot

app = Flask(__name__)
TOKEN = '7039961825:AAGmyb-lFESj2INpi81JWQAV9kgZwPBtJSU'
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных SQLite
conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def index():
    ref = request.args.get('ref')
    if ref:
        # Отправляем уведомление пользователю
        cursor.execute('SELECT chat_id FROM users WHERE chat_id = ?', (ref,))
        result = cursor.fetchone()
        if result:
            chat_id = result[0]
            bot.send_message(chat_id, "🚀 Кто-то перешел по вашей реферальной ссылке!")
    return redirect('https://braggsz.github.io/Cinema/')

if __name__ == '__main__':
    app.run(port=5000)
