from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2

app = Flask(__name__)

# Функция для подключения к базе данных
def connect_to_database():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="0167114596128Sa@",
        host="127.0.0.1",
        port="5432"
    )
    return connection

# Страница аутентификации
@app.route('/')
def index():
    return render_template('login.html')

# Проверка аутентификации
@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_name = request.form['user_name']
    password = request.form['password']

    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT user_name FROM users WHERE user_name = %s AND password = %s", (user_name, password))
    result = cursor.fetchone()

    if result:
        return redirect(url_for('tables'))
    else:
        return "Неправильное имя пользователя или пароль."

# Страница со списком таблиц
@app.route('/tables')
def tables():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [record[0] for record in cursor.fetchall()]
    return render_template('tables.html', tables=tables)

# Страница с содержимым таблицы
@app.route('/table/<table_name>')
def view_table(table_name):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()
    return render_template('table.html', table_name=table_name, records=records)

# Страница для редактирования записи в таблице
@app.route('/edit_record/<table_name>/<int:record_id>', methods=['GET', 'POST'])
def edit_record(table_name, record_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    if request.method == 'POST':
        new_data = [request.form[field] for field in request.form]
        cursor.execute(f"UPDATE {table_name} SET {', '.join([f'{field} = %s' for field in request.form])} WHERE id = %s", new_data + [record_id])
        connection.commit()
        return redirect(url_for('view_table', table_name=table_name))
    else:
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
        record = cursor.fetchone()
        return render_template('edit_record.html', table_name=table_name, record_id=record_id, record=record)
# Удаление записи
@app.route('/delete_record/<table_name>/<int:record_id>', methods=['POST'])
def delete_record(table_name, record_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
    connection.commit()
    return redirect(url_for('view_table', table_name=table_name))

@app.route('/add_record/<table_name>', methods=['GET', 'POST'])
def add_record(table_name):
    if request.method == 'POST':
        connection = connect_to_database()
        cursor = connection.cursor()
        new_data = [request.form[field] for field in request.form.keys() if field != 'id']
        columns = ', '.join(field for field in request.form.keys() if field != 'id')
        values = ', '.join('%s' for _ in request.form.keys() if _ != 'id')
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", new_data)
        connection.commit()
        return redirect(url_for('view_table', table_name=table_name))
    else:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name != 'id'", (table_name,))
        columns = [row[0] for row in cursor.fetchall()]
        return render_template('add_record.html', table_name=table_name, columns=columns)


# @app.route('/students')
# def view_students():
#     connection = connect_to_database()
#     cursor = connection.cursor()
#     cursor.execute("""
#         SELECT students.id, gruppa.name AS group_name, students.name
#         FROM students
#         JOIN gruppa ON students.group_id = gruppa.id
#     """)
#     students_data = cursor.fetchall()
#     return render_template('students.html', students=students_data)
@app.route('/table')
def show_table():
    # Ваш код для получения данных из базы данных
    table_name = "Название вашей таблицы"
    column_names = ["Название_столбца1", "Название_столбца2", ...]  # Замените на реальные названия столбцов
    records = [("значение1", "значение2", ...), ("значение1", "значение2", ...), ...]  # Замените на реальные данные из таблицы
    return render_template('your_template.html', table_name=table_name, columns=column_names, records=records)

@app.route('/students')
def view_students():
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT students.id, gruppa.name AS group_name, students.name
            FROM students
            JOIN gruppa ON students.group_id = gruppa.id
        """)
        students_data = cursor.fetchall()
        cursor.close()

        column_names = ['ID', 'Group Name', 'Student Name']

        return render_template('students.html', students=students_data, columns=column_names)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
