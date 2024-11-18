import sys
import psycopg2
import curses

class DatabaseClient:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.tables = []
        self.connection = None
        self.cursor = None

    def authenticate(self):
        self.stdscr.clear()
        self.stdscr.addstr("Введите имя пользователя: ")
        self.stdscr.refresh()
        self.user_name = self.stdscr.getstr().decode()

        self.stdscr.addstr("Введите пароль: ")
        self.stdscr.refresh()
        password = self.stdscr.getstr().decode()

        try:
            self.cursor.execute("SELECT user_name FROM users WHERE user_name = %s AND password = %s", (self.user_name, password))
            result = self.cursor.fetchone()
            if result:
                self.stdscr.addstr(f"\nВы успешно авторизованы под пользователем {self.user_name}\n")
                self.stdscr.refresh()
                self.stdscr.getch()
                return True
            else:
                self.stdscr.addstr("\nНеправильное имя пользователя или пароль.\n")
                self.stdscr.refresh()
                self.stdscr.getch()
                return False
        except psycopg2.Error as e:
            self.stdscr.addstr(f"\nОшибка аутентификации: {e}\n")
            self.stdscr.refresh()
            self.stdscr.getch()
            return False

    def populate_table_list(self):
        try:
            self.connection = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="0167114596128Sa@",
                host="127.0.0.1",
                port="5432"
            )
            self.cursor = self.connection.cursor()

            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            self.tables = [record[0] for record in self.cursor.fetchall()]
        except psycopg2.Error as e:
            self.stdscr.addstr(f"Ошибка: Невозможно подключиться к БД: {e}\n")

    def select_table(self):
        self.stdscr.clear()
        self.stdscr.addstr("Доступные таблицы:\n")
        for idx, table in enumerate(self.tables):
            self.stdscr.addstr(f"{idx + 1}. {table}\n")

        self.stdscr.addstr("\nВведите номер таблицы: ")
        self.stdscr.refresh()

        table_idx = int(self.stdscr.getstr().decode()) - 1
        table_name = self.tables[table_idx]
        self.show_table_menu(table_name)

    def show_table_menu(self, table_name):
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(f"Таблица: {table_name}\n")
            self.stdscr.addstr("Варианты:\n")
            self.stdscr.addstr("1. Просмотр таблицы\n")
            self.stdscr.addstr("2. Редактировать таблицу\n")
            self.stdscr.addstr("3. Закрыть\n")

            self.stdscr.addstr("\nВведите свой выбор: ")
            self.stdscr.refresh()

            choice = self.stdscr.getstr().decode()

            if choice == '1':
                self.view_table(table_name)
            elif choice == '2':
                self.edit_table(table_name)
            elif choice == '3':
                break
            else:
                self.stdscr.addstr("Неверный выбор. Нажмите любую кнопку, чтобы продолжить.\n")
                self.stdscr.getch()

    def view_table(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        records = self.cursor.fetchall()
        self.stdscr.clear()
        self.stdscr.addstr(f"Table: {table_name}\n")
        self.stdscr.addstr("Table Data:\n")
        for record in records:
            self.stdscr.addstr(f"{record}\n")
        self.stdscr.addstr("\nНажмите любую кнопку, чтобы продолжить.")
        self.stdscr.refresh()
        self.stdscr.getch()

    def edit_table(self, table_name):
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(f"Редактирование таблицы: {table_name}\n")
            self.stdscr.addstr("Выберите действие:\n")
            self.stdscr.addstr("1. Редактировать запись\n")
            self.stdscr.addstr("2. Добавить запись\n")
            self.stdscr.addstr("3. Удалить запись\n")
            self.stdscr.addstr("4. Назад\n")
            self.stdscr.addstr("\nВведите свой выбор: ")
            self.stdscr.refresh()

            choice = self.stdscr.getstr().decode()

            if choice == '1':
                self.edit_record(table_name)
            elif choice == '2':
                self.add_record(table_name)
            elif choice == '3':
                self.delete_record(table_name)
            elif choice == '4':
                return
            else:
                self.stdscr.addstr("Неверный выбор. Нажмите любую кнопку, чтобы продолжить.\n")
                self.stdscr.refresh()
                self.stdscr.getch()

    def edit_record(self, table_name):
        self.stdscr.clear()
        self.stdscr.addstr(f"Редактирование записи в таблице: {table_name}\n")
        self.stdscr.addstr("Введите ID записи, которую хотите отредактировать: ")
        self.stdscr.refresh()

        record_id = int(self.stdscr.getstr().decode())
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
        record = self.cursor.fetchone()

        if record:
            self.stdscr.addstr(f"Текущая запись с ID {record_id}: {record}\n")
            self.stdscr.addstr("Введите новые данные для редактирования.\n")
            self.stdscr.refresh()

            new_data = []
            for field in record:
                self.stdscr.addstr(f"Новое значение для {field}: ")
                self.stdscr.refresh()
                new_value = self.stdscr.getstr().decode()
                new_data.append(new_value)

            self.cursor.execute(f"UPDATE {table_name} SET {', '.join([f'{field} = %s' for field in record])} WHERE id = %s", new_data + [record_id])
            self.connection.commit()
            self.stdscr.addstr("Запись успешно отредактирована.\n")
        else:
            self.stdscr.addstr(f"Запись с ID {record_id} не найдена.\n")

        self.stdscr.addstr("Нажмите любую кнопку, чтобы продолжить.")
        self.stdscr.refresh()
        self.stdscr.getch()

    def add_record(self, table_name):
        self.stdscr.clear()
        self.stdscr.addstr(f"Добавление записи в таблицу: {table_name}\n")
        self.stdscr.refresh()

        try:
            self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s AND column_name != 'id'", (table_name,))
            fields = [row[0] for row in self.cursor.fetchall()]

            values = []

            for field in fields:
                self.stdscr.addstr(f"Введите значение для поля {field}: ")
                self.stdscr.refresh()
                value = self.stdscr.getstr().decode()
                values.append(value)

            fields_str = ', '.join(fields)
            placeholders_str = ', '.join(['%s'] * len(fields))

            self.cursor.execute(f"INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders_str})", values)
            self.connection.commit()

            self.stdscr.addstr("Запись успешно добавлена.\n")
        except psycopg2.Error as e:
            self.stdscr.addstr(f"Ошибка при добавлении записи: {e}\n")

        self.stdscr.addstr("Нажмите любую кнопку, чтобы продолжить.")
        self.stdscr.refresh()
        self.stdscr.getch()

    def delete_record(self, table_name):
        self.stdscr.clear()
        self.stdscr.addstr(f"Удаление записи из таблицы: {table_name}\n")
        self.stdscr.addstr("Введите ID записи, которую хотите удалить: ")
        self.stdscr.refresh()

        record_id = int(self.stdscr.getstr().decode())
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = %s", (record_id,))
        record = self.cursor.fetchone()

        if record:
            self.stdscr.addstr(f"Вы уверены, что хотите удалить запись с ID {record_id}? (y/n): ")
            self.stdscr.refresh()
            confirm = self.stdscr.getstr().decode().lower()

            if confirm == 'y':
                self.cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
                self.connection.commit()
                self.stdscr.addstr("Запись успешно удалена.\n")
            else:
                self.stdscr.addstr("Удаление отменено.\n")
        else:
            self.stdscr.addstr(f"Запись с ID {record_id} не найдена.\n")

        self.stdscr.addstr("Нажмите любую кнопку, чтобы продолжить.")
        self.stdscr.refresh()
        self.stdscr.getch()

def main(stdscr):
    try:
        client = DatabaseClient(stdscr)
        client.populate_table_list()
        client.authenticate()  # Проводим аутентификацию перед выбором таблицы
        client.select_table()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    curses.wrapper(main)
