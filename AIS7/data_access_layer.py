# data_access_layer.py
import psycopg2

class DataAccessLayer:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="0167114596128Sa@",
                host="127.0.0.1",
                port="5432"
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка: Невозможно подключиться к БД: {e}")

    def authenticate(self, user_name, password):
        try:
            self.cursor.execute("SELECT user_name FROM users WHERE user_name = %s AND password = %s", (user_name, password))
            result = self.cursor.fetchone()
            return result is not None
        except psycopg2.Error as e:
            raise Exception(f"Ошибка аутентификации: {e}")

    def get_tables(self):
        try:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            return [record[0] for record in self.cursor.fetchall()]
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении таблиц: {e}")

    def view_table(self, table_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при просмотре таблицы: {e}")

    def get_record_by_id(self, table_name, record_id):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении записи: {e}")

    def update_record(self, table_name, record_id, new_data):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
            fields = [desc[0] for desc in self.cursor.description]
            set_clause = ", ".join([f"{field} = %s" for field in fields[1:]])
            self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = %s", (*new_data, record_id))
            self.connection.commit()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при обновлении записи: {e}")

    def add_record(self, table_name, values):
        try:
            self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name != 'id'", (table_name,))
            fields = [row[0] for row in self.cursor.fetchall()]

            fields_str = ', '.join(fields)
            placeholders_str = ', '.join(['%s'] * len(fields))

            self.cursor.execute(f"INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders_str})", values)
            self.connection.commit()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при добавлении записи: {e}")

    def delete_record(self, table_name, record_id):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
            self.connection.commit()
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при удалении записи: {e}")

    def get_table_fields(self, table_name):
        try:
            self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name != 'id'", (table_name,))
            return [row[0] for row in self.cursor.fetchall()]
        except psycopg2.Error as e:
            raise Exception(f"Ошибка при получении полей таблицы: {e}")
