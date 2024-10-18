from flask import Flask, redirect
import sqlite3

app = Flask(__name__)

@app.route('/<int:ref_id>')
def redirect_to_site(ref_id):
    # Подключение к базе данных
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Обновляем данные пользователя (увеличиваем счетчик переходов)
    cursor.execute('UPDATE users SET clicks = clicks + 1 WHERE chat_id = ?', (ref_id,))
    conn.commit()
    conn.close()  # Закрываем соединение

    # Перенаправляем на ваш сайт
    return redirect("https://braggsz.github.io/Cinema/")

if __name__ == '__main__':
    app.run(debug=True)  # Включаем режим отладки
