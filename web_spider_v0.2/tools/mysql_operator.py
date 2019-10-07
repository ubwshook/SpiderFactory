"""
封装的mysql接口，主要为了提供基于字典的插入好和批量插入
"""
import pymysql


class MySqlOperator:
    def __init__(self, server, user_name, password, dbname):
        self.db_connect = pymysql.connect(server, user_name, password, dbname)
        self.cursor = self.db_connect.cursor()

    def execute(self, sql_str):
        self.cursor.execute(sql_str)
        self.db_connect.commit()
        return self.cursor

    def get_sqlstr(self, sql_dict, table_name):
        keys = [key for key in sql_dict]
        keys_str = str(keys).replace("[", '(').replace(']', ')').replace("'", "")
        value_str = ['{' + key + '}' for key in sql_dict]
        value_str = str(value_str).replace("[", '(').replace(']', ')')
        sql_str = ('INSERT INTO ' + table_name + ' ' + keys_str + ' VALUES ' + value_str).format(**sql_dict)
        return sql_str

    def insert(self, table_name, data_dict):
        sql_str = self.get_sqlstr(data_dict, table_name)
        self.cursor.execute(sql_str)
        self.db_connect.commit()

    def bulk_insert(self, table_name, data_list):
        for data in data_list:
            sql_str = self.get_sqlstr(data, table_name)
            self.cursor.execute(sql_str)
        self.db_connect.commit()
