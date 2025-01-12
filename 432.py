import sqlite3
from datetime import datetime

try:
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
except sqlite3.DatabaseError:
    print('There is a problem with Database connection')

try:
    cursor.execute("CREATE TABLE IF NOT EXISTS Stores("
                   "store_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "store_name TEXT,"
                   "address TEXT);")

    cursor.execute("CREATE TABLE IF NOT EXISTS Products("
                   "product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "store_id INTEGER,"
                   "product_name TEXT,"
                   "price REAL,"
                   "FOREIGN KEY (store_id) REFERENCES stores (store_id));"
                   )

    cursor.execute("CREATE TABLE IF NOT EXISTS Clients("
                   "client_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "client_name TEXT,"
                   "client_budget REAL);"
                   )

    cursor.execute("CREATE TABLE IF NOT EXISTS Transactions("
                   "transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "client_id INTEGER,"
                   "product_id INTEGER,"
                   "transaction_date TEXT,"
                   "FOREIGN KEY (client_id) REFERENCES clients (client_id),"
                   "FOREIGN KEY (product_id) REFERENCES clients (product_id));"
                   )
except sqlite3.ProgrammingError:
        print('Ошибка программирования')

class Store:
    @staticmethod
    def add_store(store_name, address, products):
        cursor.execute("INSERT INTO Stores(store_name, address)  VALUES(?,?)", (store_name, address))
        store_id = cursor.lastrowid
        for product in products:
            cursor.execute(
                "INSERT INTO Products (product_name, price, store_id) VALUES (?, ?, ?)",
                (product[0], product[1], store_id)
            )
        connection.commit()

    @staticmethod
    def add_product(product_name, price, store_id):
        cursor.execute("INSERT INTO Products(product_name, price, store_id) VALUES(?,?,?)",(product_name,price,store_id))
        connection.commit()

    @staticmethod
    def show_stores():
        cursor.execute("SELECT * FROM Stores;")
        result = cursor.fetchall()
        for res in result:
            print(f"ID: {res[0]}  Store Name: {res[1]}   Address: {res[2]}")


class Client:
    @staticmethod
    def add_client(client_name, client_budget):
        cursor.execute("INSERT INTO Clients(client_name, client_budget)  VALUES(?,?)", (client_name, client_budget))
        connection.commit()

    @staticmethod
    def show_clients():
        cursor.execute("SELECT * FROM Clients;")
        result = cursor.fetchall()
        for res in result:
            print(f"ID: {res[0]}  Client Name: {res[1]}   Budget: {res[2]}")

class Transaction:
    @staticmethod
    def make_purchase(client_name, store_name, product_name):
        cursor.execute("SELECT client_id, client_budget FROM Clients WHERE client_name = ?", (client_name,))
        client = cursor.fetchone()

        cursor.execute("SELECT product_id, price, store_id FROM Products WHERE product_name = ?", (product_name,))
        product = cursor.fetchone()

        if not client or not product:
            print("Клиент или продкут не найден.")
            return

        client_id, clientBudget = client
        product_id, price, store_id = product

        if clientBudget < price:
            print("У клиента недостаточно денег")
            return

        now = datetime.now()
        formatted_date = now.strftime("%d/%m/%Y")

        cursor.execute("UPDATE Clients SET client_budget = client_budget - ? WHERE client_id = ?", (price, client_id))
        cursor.execute("INSERT INTO Transactions (client_id, product_id, transaction_date) VALUES (?, ?, ?)",
                            (client_id, product_id, formatted_date))
        connection.commit()
        print(f"Покупка совершена: {client_name} купил {product_name}. Дата: {formatted_date}")