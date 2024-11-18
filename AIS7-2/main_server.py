#main_server.py
import socket
import threading
import json
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
            print("Успешное подключение к базе данных")
        except psycopg2.Error as e:
            print(f"Ошибка: Невозможно подключиться к БД: {e}")

    def authenticate(self, user_name, password):
        try:
            print(f"Попытка аутентификации для пользователя: {user_name}")
            self.cursor.execute("SELECT user_name FROM users WHERE user_name = %s AND password = %s", (user_name, password))
            result = self.cursor.fetchone()
            print(f"Результат аутентификации: {result}")
            return {"success": result is not None}
        except psycopg2.Error as e:
            print(f"Ошибка аутентификации: {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"Неожиданная ошибка при аутентификации: {e}")
            return {"error": str(e)}

    def get_tables(self):
        try:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            records = self.cursor.fetchall()
            print(f"Таблицы в базе данных: {records}")
            return {"tables": [record[0] for record in records]}
        except psycopg2.Error as e:
            print(f"Ошибка при получении таблиц: {e}")
            return {"error": str(e)}

    def view_table(self, table_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            records = self.cursor.fetchall()
            print(f"Записи в таблице {table_name}: {records}")
            return {"records": records}
        except psycopg2.Error as e:
            print(f"Ошибка при просмотре таблицы: {e}")
            return {"error": str(e)}

    def get_record_by_id(self, table_name, record_id):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
            record = self.cursor.fetchone()
            if record:
                return {"record": record}
            else:
                return {"error": f"Запись с ID {record_id} не найдена в таблице {table_name}"}
        except psycopg2.Error as e:
            print(f"Ошибка при получении записи по ID: {e}")
            return {"error": str(e)}

    def update_record(self, table_name, record_id, new_data):
        try:
            self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name != 'id'", (table_name,))
            fields = [row[0] for row in self.cursor.fetchall()]
            set_clause = ", ".join([f"{field} = %s" for field in fields])
            self.cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = %s", (*new_data, record_id))
            self.connection.commit()
            print(f"Запись с ID {record_id} в таблице {table_name} обновлена")
            return {"success": True}
        except psycopg2.Error as e:
            print(f"Ошибка при обновлении записи: {e}")
            return {"error": str(e)}

    def add_record(self, table_name, values):
        try:
            self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name != 'id'", (table_name,))
            fields = [row[0] for row in self.cursor.fetchall()]

            fields_str = ', '.join(fields)
            placeholders_str = ', '.join(['%s'] * len(fields))

            self.cursor.execute(f"INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders_str})", values)
            self.connection.commit()
            print(f"Запись добавлена в таблицу {table_name}")
            return {"success": True}
        except psycopg2.Error as e:
            print(f"Ошибка при добавлении записи: {e}")
            return {"error": str(e)}

    def delete_record(self, table_name, record_id):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
            self.connection.commit()
            print(f"Запись с ID {record_id} удалена из таблицы {table_name}")
            return {"success": True}
        except psycopg2.Error as e:
            print(f"Ошибка при удалении записи: {e}")
            return {"error": str(e)}

    def get_table_fields(self, table_name):
        try:
            self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name != 'id'", (table_name,))
            fields = [row[0] for row in self.cursor.fetchall()]
            print(f"Поля таблицы {table_name}: {fields}")
            return {"fields": fields}
        except psycopg2.Error as e:
            print(f"Ошибка при получении полей таблицы: {e}")
            return {"error": str(e)}

class BusinessLogicLayer:
    def __init__(self, data_access):
        self.data_access = data_access
        self.data_access.connect()

    def authenticate(self, user_name, password):
        return self.data_access.authenticate(user_name, password)

    def get_tables(self):
        return self.data_access.get_tables()

    def view_table(self, table_name):
        return self.data_access.view_table(table_name)

    def get_record_by_id(self, table_name, record_id):
        return self.data_access.get_record_by_id(table_name, record_id)

    def update_record(self, table_name, record_id, new_data):
        return self.data_access.update_record(table_name, record_id, new_data)

    def add_record(self, table_name, values):
        return self.data_access.add_record(table_name, values)

    def delete_record(self, table_name, record_id):
        return self.data_access.delete_record(table_name, record_id)

    def get_table_fields(self, table_name):
        return self.data_access.get_table_fields(table_name)


class Server:
    def __init__(self, host='127.0.0.1', port=12347):
        self.host = host
        self.port = port
        self.business_logic = BusinessLogicLayer(DataAccessLayer())

    def handle_client(self, client_socket):
        with client_socket as sock:
            try:
                request = sock.recv(1024).decode('utf-8')
                print(f"Получен запрос: {request}")
                response = self.process_request(request)
                print(f"Ответ на запрос: {response}")
                sock.sendall(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"Ошибка при обработке клиента: {e}")

    def process_request(self, request):
        try:
            request_data = json.loads(request)
            action = request_data.get('action')
            data = request_data.get('data')
            print(f"Обработка действия: {action} с данными: {data}")

            if action == 'authenticate':
                user_name = data.get('user_name')
                password = data.get('password')
                return self.business_logic.authenticate(user_name, password)
            elif action == 'get_tables':
                return self.business_logic.get_tables()
            elif action == 'view_table':
                table_name = data.get('table_name')
                return self.business_logic.view_table(table_name)
            elif action == 'get_record_by_id':
                table_name = data.get('table_name')
                record_id = data.get('record_id')
                return self.business_logic.get_record_by_id(table_name, record_id)
            elif action == 'update_record':
                table_name = data.get('table_name')
                record_id = data.get('record_id')
                new_data = data.get('new_data')
                return self.business_logic.update_record(table_name, record_id, new_data)
            elif action == 'add_record':
                table_name = data.get('table_name')
                values = data.get('values')
                return self.business_logic.add_record(table_name, values)
            elif action == 'delete_record':
                table_name = data.get('table_name')
                record_id = data.get('record_id')
                return self.business_logic.delete_record(table_name, record_id)
            elif action == 'get_table_fields':
                table_name = data.get('table_name')
                return self.business_logic.get_table_fields(table_name)
            else:
                return {"error": "Unknown action"}
        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            return {"error": str(e)}

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"Сервер запущен и слушает на {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Подключен клиент с адресом {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()

if __name__ == "__main__":
    server = Server()
    server.start()
