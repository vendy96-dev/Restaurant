from colorama import Fore
import sqlite3
from datetime import datetime


#Users DB
conn_users = sqlite3.connect('user_db.db')
cursor_users = conn_users.cursor()
cursor_users.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL);
""")
conn_users.commit()

#Menu DB
conn_menu = sqlite3.connect('menu_db.db')
cursor_menu = conn_menu.cursor()
cursor_menu.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    currency TEXT NOT NULL);
""")
conn_menu.commit()

#Menu DB
conn_orders = sqlite3.connect('orders_db.db')
cursor_orders = conn_orders.cursor()
cursor_orders.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    sum FLOAT NOT NULL,
    date DATE NOT NULL);
""")
conn_orders.commit()

#Check DBs if empty
cursor_users.execute('SELECT * FROM users')
print(cursor_users.fetchall())
cursor_menu.execute('SELECT * FROM menu')
print(cursor_menu.fetchall())
cursor_orders.execute('SELECT * FROM orders')
print(cursor_orders.fetchall())

#Register
account_exists = input(Fore.GREEN + 'Hello. Welcome to our coffee shop!\nDo you have a registration? (Y)es, log me in or (N)o, let me create one:\n')
while account_exists.lower() not in ['y', 'n']:
    account_exists = input("That is not a valid option! Please enter Y or N:\n")
if account_exists.lower() == 'n':
    print(Fore.RESET)
    new_username = input("Enter new username: ")
    cursor_users.execute("SELECT EXISTS (SELECT * FROM users WHERE username = ?);",(new_username,))
    result=cursor_users.fetchone()[0]
    while result:
        new_username = input("Username already exists! Please choose another one:\n")
        cursor_users.execute("SELECT EXISTS (SELECT 1 FROM users WHERE username = ?);", (new_username,))
        result = cursor_users.fetchone()[0]
    new_password = input('Enter password: ')
    new_name = input('Enter name: ')
    sql_insert_newUser = "INSERT OR IGNORE INTO users (username, password, name) VALUES (?, ?, ?)"
    cursor_users.execute(sql_insert_newUser, (new_username, new_password, new_name))
    conn_users.commit()
    print(Fore.LIGHTYELLOW_EX + f'User {new_username} registered successfully.')
    print(Fore.RESET)
    print("")
    sql_insert_existingUser = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor_users.execute(sql_insert_existingUser, (new_username, new_password))
    print(Fore.GREEN + f'Welcome, {cursor_users.fetchone()[3]}. Would you like to make a new order or view previous orders history?')
    choice = input("1. (New order)\n2. (View orders)\n")
    print(Fore.RESET)
    if choice == str(2):
        cursor_orders.execute("SELECT * FROM orders")
        row = cursor_orders.fetchone()
        while row:
            print(str(row[0])+'.', "User:", row[1], "Item:", row[2], "Quantity:", row[3], "Paid:", row[4], "BGN", "Date:", row[5])
            row = cursor_orders.fetchone()
        exit()
    elif choice == str(1):
        print('Here is our menu:')
        cursor_menu.execute('''
            INSERT OR IGNORE INTO menu (item, price, currency)
            VALUES
                ('water', '1', 'BGN'),
                ('coffee', '0.8', 'BGN'),
                ('tea', '0.5', 'BGN'),
                ('beer', '1.5', 'BGN'),
                ('soda', '1.2', 'BGN');
            ''')
        conn_menu.commit()
        cursor_menu.execute('SELECT * from menu')
        row = cursor_menu.fetchone()
        while row:
            print(row[1], row[2], row[3])
            row = cursor_menu.fetchone()

#Continue with order
    order = input("Choice:\n")
    if order == "" or order.isdigit():
        print(Fore.RED + "Order must not be a number or be blank! Aborting...")
        exit()
    cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order.lower(),))
    order_check = cursor_menu.fetchone()[0]
    while not order_check:
        order_add_new = input("That item is not on our menu. Would you like to add it? (Y)es or (N)o\n")
        while order_add_new not in ['y', 'n']:
            order_add_new = input("That is not a valid option! Please choose Y or N:\n")
        if order_add_new == 'n':
            order = input("Please choose from the existing items:\n")
            cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order.lower(),))
            order_check = cursor_menu.fetchone()[0]
        elif order_add_new == 'y':
            new_item_price = input(f'What would you like to price {order}?\n')
            sql_insert_newItem = "INSERT OR IGNORE INTO menu (item, price, currency) VALUES (?, ?, 'BGN')"
            cursor_menu.execute(sql_insert_newItem, (order, new_item_price))
            conn_menu.commit()
            print(Fore.LIGHTYELLOW_EX + f'Item {order} added to our menu!')
            sql_selected_item_price = "SELECT price FROM menu WHERE item = ?"
            cursor_menu.execute(sql_selected_item_price, (order.lower(),))
            price = cursor_menu.fetchone()
            order_count = input(f'How many {order}s would you like to order?\n')
            while order_count <= str(0):
                order_count = input("Order amount cannot be less than 1! Please enter a valid amount:\n")
            total = price[0] * float(order_count).__round__(2)
            print(Fore.LIGHTYELLOW_EX + f'You chose {order_count} {order}s. Your price is {total} BGN.')
            order_date = datetime.now().strftime('%Y-%m-%d')
            sql_insert_newOrder = "INSERT OR IGNORE INTO orders (user, item, quantity, sum, date) VALUES (?, ?, ?, ?, ?)"
            cursor_orders.execute(sql_insert_newOrder,(new_name,order.lower(), order_count, total, order_date))
            conn_orders.commit()
    if order == "" or order.isdigit():
        print(Fore.RED + "Order must not be a number or be blank! Aborting...")
        exit()
    sql_selected_item_price = "SELECT price FROM menu WHERE item = ?"
    cursor_menu.execute(sql_selected_item_price, (order.lower(),))
    price = cursor_menu.fetchone()
    order_count = input(f'How many {order}s would you like to order?\n')
    while order_count <= str(0):
        order_count=input("Order amount cannot be less than 1! Please enter a valid amount:\n")
    total = price[0] * float(order_count).__round__(2)
    print(Fore.LIGHTYELLOW_EX + f'You chose {order_count} {order}s. Your price is {total} BGN.')
    order_date = datetime.now().strftime('%Y-%m-%d')
    sql_insert_newOrder = "INSERT OR IGNORE INTO orders (user, item, quantity, sum, date) VALUES (?, ?, ?, ?, ?)"
    cursor_orders.execute(sql_insert_newOrder,(new_name, order.lower(), order_count, total, order_date))
    conn_orders.commit()

#Login
elif account_exists.lower() == 'y':
    print(Fore.RESET)
    username = input("Enter username: ")
    cursor_users.execute("SELECT EXISTS (SELECT * FROM users WHERE username = ?)", (username,))
    correct_username = cursor_users.fetchone()[0]
    password = input("Enter password: ")
    cursor_users.execute("SELECT EXISTS (SELECT 1 FROM users WHERE password = ?)", (password,))
    correct_password = cursor_users.fetchone()[0]
    if correct_username and correct_password:
        sql_insert_existingUser = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor_users.execute(sql_insert_existingUser, (username, password))
        current_user = cursor_users.fetchone()[3]
        print(Fore.GREEN + f'Welcome, {current_user}. Would you like to make a new order or view previous orders history?')
        choice = input("1. (New order)\n2. (View orders)\n")
        print(Fore.RESET)
        if choice == str(2):
            cursor_orders.execute("SELECT * FROM orders")
            row = cursor_orders.fetchone()
            while row:
                print(str(row[0])+'.', "User:", row[1], "Item:",row[2], "Quantity:",row[3], "Paid:",row[4], "BGN", "Date:",row[5])
                row = cursor_orders.fetchone()
            exit()
        elif choice == str(1):
            print('Here is our menu:')
            cursor_menu.execute('''
            INSERT OR IGNORE INTO menu (item, price, currency) 
            VALUES
            ('water', '1', 'BGN'),
            ('coffee', '0.8', 'BGN'),
            ('tea', '0.5', 'BGN'),
            ('beer', '1.5', 'BGN'),
            ('soda', '1.2', 'BGN');
            ''')
            conn_menu.commit()
            print(Fore.RESET)
            cursor_menu.execute('SELECT * from menu')
            row = cursor_menu.fetchone()
            while row:
                print(row[1], row[2], row[3])
                row = cursor_menu.fetchone()

#Continue with order
        order = input("Choice:\n")
        if order == "" or order.isdigit():
            print(Fore.RED + "Order must not be a number or be blank! Aborting...")
            exit()
        cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order.lower(),))
        order_check = cursor_menu.fetchone()[0]
        while not order_check:
            order_add_new = input("That item is not on our menu. Would you like to add it? (Y)es or (N)o\n")
            if order_add_new == 'n':
                order = input("Please choose from the existing items:\n")
                cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order.lower(),))
                order_check = cursor_menu.fetchone()[0]
            elif order_add_new == 'y':
                new_item_price = input(f'What would you like to price {order}?\n')
                sql_insert_newItem = "INSERT OR IGNORE INTO menu (item, price, currency) VALUES (?, ?, 'BGN')"
                cursor_menu.execute(sql_insert_newItem, (order.lower(), new_item_price))
                conn_menu.commit()
                print(Fore.LIGHTYELLOW_EX + f'Item {order} added to our menu!')
                print(Fore.RESET)
                cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order.lower(),))
                order_check = cursor_menu.fetchone()[0]
        sql_selected_item_price = "SELECT price FROM menu WHERE item = ?"
        cursor_menu.execute(sql_selected_item_price, (order.lower(),))
        price = cursor_menu.fetchone()
        order_count = input(f'How many {order}s would you like to order?\n')
        while order_count <= str(0):
            order_count = input(Fore.RED + "Order amount cannot be less than 1! Please enter a valid amount:\n")
        total = price[0] * float(order_count).__round__(2)
        print(Fore.LIGHTYELLOW_EX + f'You chose {order_count} {order}s. Your price is {total} BGN.')
        order_date = datetime.now().strftime('%Y-%m-%d')
        sql_insert_newOrder = "INSERT OR IGNORE INTO orders (user, item, quantity, sum, date) VALUES (?, ?, ?, ?, ?)"
        cursor_orders.execute(sql_insert_newOrder,(current_user,order.lower(), order_count, total, order_date))
        conn_orders.commit()
    else:
        print(Fore.RED + f'Username or password is incorrect! Aborting...')

#End program
input(Fore.GREEN + "Have a nice day! Press enter key...")
# cursor_menu.execute('DELETE FROM menu')
# cursor_menu.execute("DELETE FROM sqlite_sequence WHERE name = 'menu';")
# conn_menu.commit()
# cursor_users.execute('DELETE FROM users')
# cursor_users.execute("DELETE FROM sqlite_sequence WHERE name = 'users';")
# conn_users.commit()
# cursor_orders.execute('DELETE FROM orders')
# cursor_menu.execute("DELETE FROM sqlite_sequence WHERE name = 'orders';")
# conn_orders.commit()

#Close DB connections
conn_users.close()
conn_menu.close()
conn_orders.close()
