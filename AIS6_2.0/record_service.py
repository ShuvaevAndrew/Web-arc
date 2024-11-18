from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2

record_blueprint = Blueprint('record', __name__)

def connect_to_database():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="0167114596128Sa@",
        host="127.0.0.1",
        port="5432"
    )
    return connection

@record_blueprint.route('/add_record/<table_name>', methods=['GET', 'POST'])
def add_record(table_name):
    if request.method == 'POST':
        connection = connect_to_database()
        cursor = connection.cursor()
        new_data = [request.form[field] for field in request.form.keys()]
        columns = ', '.join(request.form.keys())
        values = ', '.join('%s' for _ in request.form.keys())
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", new_data)
        connection.commit()
        return redirect(url_for('table.view_table', table_name=table_name))
    else:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name != 'id'", (table_name,))
        columns = [row[0] for row in cursor.fetchall()]
        return render_template('add_record.html', table_name=table_name, columns=columns)

@record_blueprint.route('/edit_record/<table_name>/<int:record_id>', methods=['GET', 'POST'])
def edit_record(table_name, record_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Exclude the 'id' field from the update
        form_data.pop('id', None)
        
        # Prepare the update statement
        columns = ', '.join([f"{field} = %s" for field in form_data.keys()])
        values = list(form_data.values())
        
        # Execute the update statement
        cursor.execute(f"UPDATE {table_name} SET {columns} WHERE id = %s", values + [record_id])
        connection.commit()
        return redirect(url_for('table.view_table', table_name=table_name))
    else:
        cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
        record = cursor.fetchone()
        record_dict = dict(zip([desc[0] for desc in cursor.description], record))
        return render_template('edit_record.html', table_name=table_name, record_id=record_id, record=record_dict)

@record_blueprint.route('/delete_record/<table_name>/<int:record_id>', methods=['POST'])
def delete_record(table_name, record_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
    connection.commit()
    return redirect(url_for('table.view_table', table_name=table_name))
