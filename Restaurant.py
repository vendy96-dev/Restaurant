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
    item TEXT NOT NULL,
    price FLOAT NOT NULL,
    currency TEXT NOT NULL);
""")
conn_menu.commit()

#Check DBs if empty
cursor_users.execute('SELECT * FROM users')
print(cursor_users.fetchall())
cursor_menu.execute('SELECT * FROM menu')
print(cursor_menu.fetchall())


#Variables
price = 0
total = 0
newPrice = 0
numberOfOrders = 0
newTotal = 0
oldItemChoice = ""
oldItemNumberOfOrders = 0


#Register
account_exists = input('Hello. Welcome to our coffee shop!\nDo you have a registration? (Y)es, log me in or (N)o, let me create one:\n')
if account_exists.lower() == 'n':
    new_username = input("Enter new username: ")
    new_password = input('Enter password: ')
    new_name = input('Enter name: ')
    sql_insert_newUser = "INSERT OR IGNORE INTO users (username, password, name) VALUES (?, ?, ?)"
    cursor_users.execute(sql_insert_newUser, (new_username, new_password, new_name))
    conn_users.commit()
    print("User registered successfully.")
    print("")
    sql_insert_existingUser = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor_users.execute(sql_insert_existingUser, (new_username, new_password))
    print(f'Welcome, {cursor_users.fetchone()[3]}. Here is our menu: ')
    cursor_menu.execute('''
        INSERT INTO menu (item, price, currency) 
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

    #Configure orders...!!

elif account_exists.lower() == 'y':
    username = input("Enter username: ")
    password = input("Enter password: ")
    sql_insert_existingUser = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor_users.execute(sql_insert_existingUser, (username, password))
    print(f'Welcome, {cursor_users.fetchone()[3]}. What would you like to order?: ')
    cursor_menu.execute('''
    INSERT INTO menu (item, price, currency) 
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
    order = input("Choice (item or number of item):\n")
    if order == "":
        print(Fore.RED + "Order must not be blank! Aborting...")
        exit()
    if order.lower() == 'water' or order == 1:
             price = 1
#             total = price * float(oldItemNumberOfOrders).__round__(2)
#             print(f'You chose {oldItemNumberOfOrders} {menu[0]}s. Your price is {total} BGN.')
    # #if order not in menu:
    #     addNew = input('We do not have that in our menu. Would you like to add it? (Y)es or (N)o:\n')
    #     if addNew.lower() == 'n':
    #         print(*menu)
    #         oldItemChoice = input('Please choose another item of the available ones from our menu:\n')
    #         if oldItemChoice not in menu:
    #             print(Fore.RED + 'Your order will be cancelled. We are sorry for the inconvenience!')
    #             exit()
    #         oldItemNumberOfOrders = input(f'How many {oldItemChoice}s would you like to order?\n')
    #         if not oldItemNumberOfOrders.isdigit():
    #             print(Fore.RED + 'Number of items should be a digit and not be blank! Aborting...')
    #             exit()
    #         if oldItemChoice.lower() == 'water':
    #             price = 1
    #             total = price * float(oldItemNumberOfOrders).__round__(2)
    #             print(f'You chose {oldItemNumberOfOrders} {menu[0]}s. Your price is {total} BGN.')
    #         elif oldItemChoice.lower() == 'coffee':
    #             price = 0.8
    #             total = price * float(oldItemNumberOfOrders).__round__(2)
    #             print(f'You chose {oldItemNumberOfOrders} {menu[2]}s. Your price is {total} BGN.')
    #         elif oldItemChoice.lower() == 'tea':
    #             price = 0.5
    #             total = price * float(oldItemNumberOfOrders).__round__(2)
    #             print(f'You chose {oldItemNumberOfOrders} {menu[4]}s. Your price is {total} BGN.')
    #         elif oldItemChoice.lower() == 'beer':
    #             price = 1.5
    #             total = price * float(oldItemNumberOfOrders).__round__(2)
    #             print(f'You chose {oldItemNumberOfOrders} {menu[6]}s. Your price is {total} BGN.')
    #         elif oldItemChoice.lower() == 'soda':
    #             price = 1.2
    #             total = price * float(oldItemNumberOfOrders).__round__(2)
    #             print(f'You chose {oldItemNumberOfOrders} {menu[8]}s. Your price is {total} BGN.')
    #         menu.append(order)
    #         input()
    #         exit()
    #     elif addNew.lower() == "y":
    #         print(f"What would the price of {order} be?")
    #         newPrice = input()
    #         if newPrice == "":
    #             print(Fore.RED + 'Price cannot be blank! Aborting...')
    #             exit()
    #         addItem = "- " + newPrice + " BGN"
    #         menu.extend([order,addItem])
    #         print(Fore.RED + 'Our updated menu now includes: ')
    #         print(*menu)
    #         print(Fore.RESET)
    #         numberOfOrders = input(f'How many {order}s would you like to order?\n')
    #         if not numberOfOrders.isdigit():
    #             print(Fore.RED + 'Number of items should be a digit and not be blank! Aborting...')
    #             exit()
    #         newTotal = float(newPrice.strip(" - BGN")) * float(numberOfOrders)
    #         print(f'Great! Your total for {numberOfOrders} {order}s is {newTotal} BGN.')
    #         input()
    #         exit()
    #     else:
    #         print(Fore.RED + "That is not a valid option! Aborting...")
    #         exit()
    # oldItemNumberOfOrders = input(f'How many {order}s would you like to order?\n')
    # if not oldItemNumberOfOrders.isdigit():
    #     print(Fore.RED + 'Number of items should be a digit and not be blank! Aborting...')
    #     exit()
    # if order.lower() == 'water':
    #              price = 1
    #              total = price * float(oldItemNumberOfOrders).__round__(2)
    #              print(f'You chose {oldItemNumberOfOrders} {menu[0]}s. Your price is {total} BGN.')
    # elif order.lower() == 'coffee':
    #              price = 0.8
    #              total = price * float(oldItemNumberOfOrders).__round__(2)
    #              print(f'You chose {oldItemNumberOfOrders} {menu[2]}s. Your price is {total} BGN.')
    # elif order.lower() == 'tea':
    #              price = 0.5
    #              total = price * float(oldItemNumberOfOrders).__round__(2)
    #              print(f'You chose {oldItemNumberOfOrders} {menu[4]}s. Your price is {total} BGN.')
    # elif order.lower() == 'beer':
    #              price = 1.5
    #              total = price * float(oldItemNumberOfOrders).__round__(2)
    #              print(f'You chose {oldItemNumberOfOrders} {menu[6]}s. Your price is {total} BGN.')
    # elif order.lower() == 'soda':
    #              price = 1.2
    #              total = price * float(oldItemNumberOfOrders).__round__(2)
    #              print(f'You chose {oldItemNumberOfOrders} {menu[8]}s. Your price is {total} BGN.')
    # else:
    #     print(Fore.RED + "That is not a valid option! Aborting...")
    #     exit()
input("Have a nice day! Press enter key...")
cursor_menu.execute('DROP TABLE menu')
conn_menu.commit()
#cursor_users.execute('DROP TABLE users')
#conn_users.commit()
conn_users.close()
conn_menu.close()
