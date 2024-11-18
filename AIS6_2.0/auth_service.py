from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2

auth_blueprint = Blueprint('auth', __name__)

def connect_to_database():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="0167114596128Sa@",
        host="127.0.0.1",
        port="5432"
    )
    return connection

@auth_blueprint.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']

        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT user_name FROM users WHERE user_name = %s AND password = %s", (user_name, password))
        result = cursor.fetchone()
           
        if result:
            return redirect(url_for('table.view_tables'))
        else:
            return "Неправильное имя пользователя или пароль."
    else:
        return render_template('login.html')