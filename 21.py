import sqlite3
from datetime import datetime

connection = sqlite3.connect("to_do.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Tasks(" 
               "id INTEGER PRIMARY KEY AUTOINCREMENT," 
               "name TEXT," 
               "status BOOLEAN, " 
               "date TEXT);")

class Task:
    def __init__(self,name,status,date):
        self.name = name
        self.status = status
        self.date = date

    @staticmethod
    def add_task(name, status, date):
        cursor.execute("INSERT INTO tasks (name, status,date)  VALUES(?,?,?)", (name, status, date))
        print(f"Задача под названием {name} успешно добавлена в базу данных")
        connection.commit()

Task.add_task("Помыть посуду", True, "24.11.2024 19:00")
connection.close()