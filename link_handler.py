from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Подключение к базе данных
conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def index():
    return "Welcome to the link tracking service!"

@app.route('/Cinema/')
def track_link():
    ref_hash = request.args.get('ref')
    
    if ref_hash:
        # Сохраняем информацию о переходе в базе данных
        cursor.execute('INSERT INTO link_clicks (user_hash) VALUES (?)', (ref_hash,))
        conn.commit()

        # Здесь можно добавить уведомление пользователю (например, через Telegram)

    # Перенаправляем на основной сайт
    return redirect("https://braggsz.github.io/Cinema/")

if __name__ == "__main__":
    app.run(port=5000)
