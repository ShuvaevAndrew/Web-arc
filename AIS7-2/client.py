import socket
import json

class Client:
    def __init__(self, server_host='127.0.0.1', server_port=12347):
        self.server_host = server_host
        self.server_port = server_port
        self.authenticated = False

    def send_request(self, action, data):
        try:
            request = json.dumps({"action": action, "data": data})
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.server_host, self.server_port))
                sock.sendall(request.encode('utf-8'))
                response = sock.recv(1024).decode('utf-8')
                return json.loads(response)
        except Exception as e:
            return {"error": str(e)}

    def authenticate(self, user_name, password):
        response = self.send_request("authenticate", {"user_name": user_name, "password": password})
        if response.get("success"):
            self.authenticated = True
        return response

    def get_tables(self):
        return self.send_request("get_tables", {})

    def view_table(self, table_name):
        return self.send_request("view_table", {"table_name": table_name})

    def get_record_by_id(self, table_name, record_id):
        return self.send_request("get_record_by_id", {"table_name": table_name, "record_id": record_id})

    def update_record(self, table_name, record_id, new_data):
        return self.send_request("update_record", {"table_name": table_name, "record_id": record_id, "new_data": new_data})

    def add_record(self, table_name, values):
        return self.send_request("add_record", {"table_name": table_name, "values": values})

    def delete_record(self, table_name, record_id):
        return self.send_request("delete_record", {"table_name": table_name, "record_id": record_id})

    def get_table_fields(self, table_name):
        return self.send_request("get_table_fields", {"table_name": table_name})

if __name__ == "__main__":
    server_host = input("Введите IP-адрес сервера: ")
    server_port = int(input("Введите порт сервера: "))

    client = Client(server_host, server_port)
    
    while True:
        print("\nВыберите действие:")
        if not client.authenticated:
            print("1. Аутентификация")
        print("2. Получить список таблиц")
        print("3. Просмотреть таблицу")
        print("4. Получить запись по ID")
        print("5. Обновить запись")
        print("6. Добавить запись")
        print("7. Удалить запись")
        print("8. Получить поля таблицы")
        print("9. Выход")
        
        choice = input("Введите номер действия: ")

        if choice == '1' and not client.authenticated:
            user_name = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            response = client.authenticate(user_name, password)
            print("Ответ:", response)
        
        elif client.authenticated:
            if choice == '2':
                response = client.get_tables()
                print("Ответ:", response)
            
            elif choice == '3':
                table_name = input("Введите имя таблицы: ")
                response = client.view_table(table_name)
                print("Ответ:", response)
            
            elif choice == '4':
                table_name = input("Введите имя таблицы: ")
                try:
                    record_id = int(input("Введите ID записи: "))
                    response = client.get_record_by_id(table_name, record_id)
                    print("Ответ:", response)
                except ValueError:
                    print("Ошибка: ID записи должно быть числом.")
            
            elif choice == '5':
                table_name = input("Введите имя таблицы: ")
                try:
                    record_id = int(input("Введите ID записи: "))
                    new_data = input("Введите новые данные (через запятую): ").split(',')
                    response = client.update_record(table_name, record_id, new_data)
                    print("Ответ:", response)
                except ValueError:
                    print("Ошибка: ID записи должно быть числом.")
            
            elif choice == '6':
                table_name = input("Введите имя таблицы: ")
                values = input("Введите значения (через запятую): ").split(',')
                response = client.add_record(table_name, values)
                print("Ответ:", response)
            
            elif choice == '7':
                table_name = input("Введите имя таблицы: ")
                try:
                    record_id = int(input("Введите ID записи: "))
                    response = client.delete_record(table_name, record_id)
                    print("Ответ:", response)
                except ValueError:
                    print("Ошибка: ID записи должно быть числом.")
            
            elif choice == '8':
                table_name = input("Введите имя таблицы: ")
                response = client.get_table_fields(table_name)
                print("Ответ:", response)
            
            elif choice == '9':
                print("Выход из программы.")
                break
            
            else:
                print("Неверный выбор, попробуйте снова.")
        
        else:
            print("Для выполнения этого действия необходимо аутентифицироваться.")
            
        if choice == '9':
            print("Выход из программы.")
            break
