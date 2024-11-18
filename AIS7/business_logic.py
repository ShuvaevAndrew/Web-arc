class BusinessLogicLayer:
    def __init__(self, data_access):
        self.data_access = data_access

    def authenticate(self, user_name, password):
        return self.data_access.authenticate(user_name, password)

    def get_tables(self):
        return self.data_access.get_tables()

    def view_table(self, table_name):
        return self.data_access.view_table(table_name)

    def get_record_by_id(self, table_name, record_id):
        return self.data_access.get_record_by_id(table_name, record_id)

    def update_record(self, table_name, record_id, new_data):
        self.data_access.update_record(table_name, record_id, new_data)

    def add_record(self, table_name, values):
        self.data_access.add_record(table_name, values)

    def delete_record(self, table_name, record_id):
        self.data_access.delete_record(table_name, record_id)

    def get_table_fields(self, table_name):
        return self.data_access.get_table_fields(table_name)
