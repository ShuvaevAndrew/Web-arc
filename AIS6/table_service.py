from flask import Blueprint, render_template
import psycopg2

table_blueprint = Blueprint('table', __name__)

def connect_to_database():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="0167114596128Sa@",
        host="127.0.0.1",
        port="5432"
    )
    return connection

@table_blueprint.route('/tables')
def view_tables():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [record[0] for record in cursor.fetchall()]
    return render_template('tables.html', tables=tables)

@table_blueprint.route('/table/<table_name>')
def view_table(table_name):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()

    # Get column names from cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Add the `editing_enabled` variable here
    editing_enabled = True  # Change this to False to disable editing

    return render_template('table.html', table_name=table_name, column_names=column_names, records=records, editing_enabled=editing_enabled)
