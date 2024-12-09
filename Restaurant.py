from colorama import Fore
import sqlite3


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

#Check DBs if empty
cursor_users.execute('SELECT * FROM users')
print(cursor_users.fetchall())
cursor_menu.execute('SELECT * FROM menu')
print(cursor_menu.fetchall())

#Register
account_exists = input(Fore.GREEN + 'Hello. Welcome to our coffee shop!\nDo you have a registration? (Y)es, log me in or (N)o, let me create one:\n')
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
    print(f'Welcome, {cursor_users.fetchone()[3]}. What would you like to order?\n')
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
        print(*row)
        row = cursor_menu.fetchone()

#Continue with order
    order = input("Choice:\n")
    if order == "" or order.isdigit():
        print(Fore.RED + "Order must not be a number or be blank! Aborting...")
        exit()
    cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order,))
    order_check = cursor_menu.fetchone()[0]
    while not order_check:
        order_add_new = input("That item is not on our menu. Would you like to add it? (Y)es or (N)o\n")
        if order_add_new == 'n':
            order = input("Please choose from the existing items:\n")
            cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order,))
            order_check = cursor_menu.fetchone()[0]
        elif order_add_new == 'y':
            new_item_price = input(f'What would you like to price {order}?\n')
            sql_insert_newItem = "INSERT OR IGNORE INTO menu (item, price, currency) VALUES ('?', '?', 'BGN')"
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
        print(Fore.GREEN + f'Welcome, {cursor_users.fetchone()[3]}. What would you like to order?\n')
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
            print(*row)
            row = cursor_menu.fetchone()

#Continue with order
        order = input("Choice:\n")
        if order == "" or order.isdigit():
            print(Fore.RED + "Order must not be a number or be blank! Aborting...")
            exit()
        cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order,))
        order_check = cursor_menu.fetchone()[0]
        while not order_check:
            order_add_new = input("That item is not on our menu. Would you like to add it? (Y)es or (N)o\n")
            if order_add_new == 'n':
                order = input("Please choose from the existing items:\n")
                cursor_menu.execute("SELECT EXISTS (SELECT 1 FROM menu WHERE item = ?)", (order,))
                order_check = cursor_menu.fetchone()[0]
            elif order_add_new == 'y':
                new_item_price = input(f'What would you like to price {order}?\n')
                sql_insert_newItem = "INSERT OR IGNORE INTO menu (item, price, currency) VALUES ('?', '?', 'BGN')"
                cursor_menu.execute(sql_insert_newItem, (order, new_item_price))
                conn_menu.commit()
                print(Fore.LIGHTYELLOW_EX + f'Item {order} added to our menu!')
        sql_selected_item_price = "SELECT price FROM menu WHERE item = ?"
        cursor_menu.execute(sql_selected_item_price, (order.lower(),))
        price = cursor_menu.fetchone()
        order_count = input(f'How many {order}s would you like to order?\n')
        while order_count <= str(0):
            order_count = input(Fore.RED + "Order amount cannot be less than 1! Please enter a valid amount:\n")
        total = price[0] * float(order_count).__round__(2)
        print(Fore.LIGHTYELLOW_EX + f'You chose {order_count} {order}s. Your price is {total} BGN.')
    else:
        print(Fore.RED + f'Username or password is incorrect! Aborting...')

input(Fore.GREEN + "Have a nice day! Press enter key...")
# cursor_menu.execute('DELETE FROM menu')
# cursor_menu.execute("DELETE FROM sqlite_sequence WHERE name = 'menu';")
# cursor_menu.execute("DROP TABLE menu")
# conn_menu.commit()
# cursor_users.execute('DELETE FROM users')
# cursor_users.execute("DELETE FROM sqlite_sequence WHERE name = 'users';")
# conn_users.commit()
conn_users.close()
conn_menu.close()
