import requests
from flask import Flask, render_template, request
import psycopg2
app = Flask(__name__)
conn = psycopg2.connect(database="nana",
                        user="postgres",
                        password="5050",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())

    # не введено имя пользователя
    if not username:
        not_field = 'Заполните поле "Username".'
        return render_template('login.html', not_field=not_field)

    # не введён пароль
    if not password:
        not_field = 'Заполните поле "Password".'
        return render_template('login.html', not_field=not_field)

    # пользователь не найден
    if not records:
        return render_template('error_form.html')
    else:
        return render_template('account.html', full_name=records[0][1], login=username, password=password)


if __name__ == '__main__':
    app.run()