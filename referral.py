from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Подключение к базе данных SQLite
conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/referral/<int:chat_id>')
def referral(chat_id):
    import requests
    TOKEN = '7039961825:AAGmyb-lFESj2INpi81JWQAV9kgZwPBtJSU'
    
    cursor.execute('SELECT name FROM users WHERE chat_id = ?', (chat_id,))
    user = cursor.fetchone()

    if user:
        user_name = user[0]
        message = f"👤 {user_name}, по вашей ссылке перешёл человек!"
        
        # Отправляем сообщение пользователю
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data={
            'chat_id': chat_id,
            'text': message
        })

    return "Уведомление отправлено", 200  # Возвращаем ответ на запрос

if __name__ == '__main__':
    app.run(port=5000)
