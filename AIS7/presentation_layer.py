import curses

class PresentationLayer:
    def __init__(self, stdscr, business_logic):
        self.stdscr = stdscr
        self.business_logic = business_logic

    def authenticate(self):
        self.stdscr.clear()
        self.stdscr.addstr("Введите имя пользователя: ")
        self.stdscr.refresh()
        user_name = self.stdscr.getstr().decode()

        self.stdscr.addstr("Введите пароль: ")
        self.stdscr.refresh()
        password = self.stdscr.getstr().decode()

        success = self.business_logic.authenticate(user_name, password)

        if success:
            self.stdscr.addstr(f"\nВы успешно авторизованы под пользователем {user_name}\n")
        else:
            self.stdscr.addstr("\nНеправильное имя пользователя или пароль.\n")

        self.stdscr.refresh()
        self.stdscr.getch()

        return success

    def display_tables(self):
        tables = self.business_logic.get_tables()
        self.stdscr.clear()
        self.stdscr.addstr("Доступные таблицы:\n")
        for idx, table in enumerate(tables):
            self.stdscr.addstr(f"{idx + 1}. {table}\n")

        self.stdscr.addstr("\nВведите номер таблицы: ")
        self.stdscr.refresh()
        table_idx = int(self.stdscr.getstr().decode()) - 1
        table_name = tables[table_idx]
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
        records = self.business_logic.view_table(table_name)
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
        record = self.business_logic.get_record_by_id(table_name, record_id)

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

            self.business_logic.update_record(table_name, record_id, new_data)
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

        fields = self.business_logic.get_table_fields(table_name)
        values = []

        for field in fields:
            self.stdscr.addstr(f"Введите значение для поля {field}: ")
            self.stdscr.refresh()
            value = self.stdscr.getstr().decode()
            values.append(value)

        self.business_logic.add_record(table_name, values)
        self.stdscr.addstr("Запись успешно добавлена.\n")
        self.stdscr.addstr("Нажмите любую кнопку, чтобы продолжить.")
        self.stdscr.refresh()
        self.stdscr.getch()

    def delete_record(self, table_name):
        self.stdscr.clear()
        self.stdscr.addstr(f"Удаление записи из таблицы: {table_name}\n")
        self.stdscr.addstr("Введите ID записи, которую хотите удалить: ")
        self.stdscr.refresh()

        record_id = int(self.stdscr.getstr().decode())
        record = self.business_logic.get_record_by_id(table_name, record_id)

        if record:
            self.stdscr.addstr(f"Вы уверены, что хотите удалить запись с ID {record_id}? (y/n): ")
            self.stdscr.refresh()
            confirm = self.stdscr.getstr().decode().lower()

            if confirm == 'y':
                self.business_logic.delete_record(table_name, record_id)
                self.stdscr.addstr("Запись успешно удалена.\n")
            else:
                self.stdscr.addstr("Удаление отменено.\n")
        else:
            self.stdscr.addstr(f"Запись с ID {record_id} не найдена.\n")

        self.stdscr.addstr("Нажмите любую кнопку, чтобы продолжить.")
        self.stdscr.refresh()
        self.stdscr.getch()
