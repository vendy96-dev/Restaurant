import sqlite3
from datetime import datetime
from customtkinter import *
from tkinter import messagebox, ttk, PhotoImage
import logging

logging.basicConfig(
    filename='./logfile.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')



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
cursor_menu.execute('''
            INSERT OR IGNORE INTO menu (item, price, currency) 
            VALUES
            ('water', '1', 'BGN'),
            ('coffee', '0.8', 'BGN'),
            ('tea', '0.5', 'BGN'),
            ('beer', '1.5', 'BGN'),
            ('soda', '1.2', 'BGN'),
            ('burger', '5', 'BGN'),
            ('pizza', '10', 'BGN'),
            ('sandwich', '4.5', 'BGN'),
            ('macaroni', '6', 'BGN'),
            ('omelette', '3.5', 'BGN'),
            ('sausage', '2', 'BGN');
            ''')
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


#Login Screen
def home_login_button_click(): #Login button on the home screen
    login_window = CTkToplevel()
    login_window.title("Login")
    login_window.geometry('400x350')
    icon = PhotoImage(file="E:\PythonProjects\Restaurant\Restaurant.png")
    login_window.iconphoto(False,icon)
    login_window.resizable(False, False)
    login_window.focus_set()
    home_window.withdraw()

    login_window_frame = CTkFrame(login_window, width=300,height=200, corner_radius=15)
    login_window_frame.pack(padx=20,pady=20)

    login_window_label = CTkLabel(login_window_frame, text='Login', font=("Arial",20,'italic'), text_color='#bf2459')
    login_window_label.grid(row=0, column=0, padx=15, pady=10)

    entry_login_name = CTkEntry(master=login_window_frame, placeholder_text='Username...')
    entry_login_name.grid(row=1, column=0, padx=15, pady=10)

    entry_login_password = CTkEntry(master=login_window_frame, placeholder_text='Password...', show='*')
    entry_login_password.grid(row=2, column=0, padx=15, pady=10)

    btn_login = CTkButton(master=login_window_frame, text='Login', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=lambda: btn_login_window_click(entry_login_name, entry_login_password,login_window))
    btn_login.grid(row=3, column=0, padx=15, pady=10)

    btn_login_cancel = CTkButton(master=login_window_frame, text='Cancel', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command = lambda: login_window_cancel_click(home_window, login_window))
    btn_login_cancel.grid(row=4, column=0, padx=15, pady=10)

def login_window_cancel_click(home_window, login_window): #Cancel button on login window
    home_window.deiconify()
    login_window.destroy()

#Main Menu Screen
def btn_login_window_click(entry_login_name, entry_login_password, login_window): #Login function in login window
    username = entry_login_name.get()
    password = entry_login_password.get()

    cursor_users.execute("SELECT EXISTS (SELECT * FROM users WHERE username = ?)", (username,))
    correct_username = cursor_users.fetchone()[0]
    cursor_users.execute("SELECT EXISTS (SELECT 1 FROM users WHERE password = ?)", (password,))
    correct_password = cursor_users.fetchone()[0]

    if correct_username and correct_password:
        sql_insert_existingUser = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor_users.execute(sql_insert_existingUser, (username, password))
        current_user = cursor_users.fetchone()[3]
        messagebox.showinfo('Success', f'Welcome, {current_user}.')
        login_window.destroy()

        main_menu_window = CTkToplevel()
        main_menu_window.title("Main Menu")
        main_menu_window.iconbitmap('E:\PythonProjects\Restaurant\Restaurant.png')
        main_menu_window.geometry('400x350')
        main_menu_window.resizable(False, False)

        main_menu_frame = CTkFrame(main_menu_window, width=300, height=200, corner_radius=15)
        main_menu_frame.pack(padx=20,pady=20)

        main_menu_label = CTkLabel(main_menu_frame, text="Main Menu", font=("Arial",20,'italic'), text_color='#bf2459')
        main_menu_label.grid(row=0, column=0, padx=15, pady=10)

        btn_new_order = CTkButton(master=main_menu_frame, text='New Order', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=lambda:btn_new_order_click(new_name=current_user))
        btn_new_order.grid(row=1, column=0, padx=15, pady=10)

        btn_orders_history = CTkButton(master=main_menu_frame, text='Order History', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=lambda: button_orders_history_click(main_menu_window))
        btn_orders_history.grid(row=2, column=0, padx=15, pady=10)

        btn_orders_logout = CTkButton(master=main_menu_frame, text='Logout', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command= lambda: btn_orders_logout_click(home_window,main_menu_window))
        btn_orders_logout.grid(row=3, column=0, padx=15, pady=10)

        home_window.withdraw()
    else:
        messagebox.showwarning('Error','Username or password incorrect!')

def btn_new_order_click(new_name): #New order button on Main Menu
    conn = sqlite3.connect('menu_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT item FROM menu')
    items = cursor.fetchall()

    item_list = []
    for item in items:
        item_list.append(item[0].ljust(1))

    new_order_window = CTkToplevel()
    new_order_window.title("New Order")
    icon = PhotoImage(file='E:\PythonProjects\Restaurant\Restaurant.png')
    new_order_window.iconphoto(False, icon)
    new_order_window.geometry('400x350')
    new_order_window.resizable(False, False)

    new_order_frame = CTkFrame(new_order_window, width=300, height=200, corner_radius=15)
    new_order_frame.pack(padx=20,pady=20)

    new_order_label = CTkLabel(new_order_frame, text='New Order', font=("Arial",20,'italic'), text_color='#bf2459')
    new_order_label.grid(row=1, column=0, padx=15, pady=10)

    combobox_item = CTkComboBox(master=new_order_frame, values=item_list)
    combobox_item.grid(row=2, column=0, padx=15, pady=10)

    entry_quantity = CTkEntry(master=new_order_frame, placeholder_text='Quantity...')
    entry_quantity.grid(row=3, column=0, padx=15, pady=10)

    btn_place_order = CTkButton(master=new_order_frame, text='Place Order', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=lambda:btn_place_order_click(new_name, combobox_item.get(), entry_quantity.get()))
    btn_place_order.grid(row=4, column=0, padx=15, pady=10)

    btn_new_order_cancel = CTkButton(master=new_order_frame, text='Cancel', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=new_order_window.destroy)
    btn_new_order_cancel.grid(row=5, column=0, padx=15, pady=10)

def btn_place_order_click(new_name, order, quantity):
   conn_menu = sqlite3.connect('menu_db.db')
   cursor_menu = conn_menu.cursor()
   conn_orders = sqlite3.connect('orders_db.db')
   cursor_orders = conn_orders.cursor()
   order_date = datetime.now().strftime('%Y-%m-%d')
   sql_select_item = 'SELECT price FROM menu WHERE item = ?'
   cursor_menu.execute(sql_select_item, (order.lower(),))
   price = cursor_menu.fetchone()
   try:
    total = price[0] * float(quantity)
    result=messagebox.askyesno('Confirm', f'You chose {quantity} {order}s for a total of {total:.2f} BGN.\nDo you accept?')
    if result:
        sql_insert_newOrder = "INSERT OR IGNORE INTO orders (user, item, quantity, sum, date) VALUES (?, ?, ?, ?, ?)"
        cursor_orders.execute(sql_insert_newOrder, (new_name, order.lower(), quantity, total, order_date))
        conn_orders.commit()
        messagebox.showinfo("Info", 'Order placed successfully.')
    else:
        messagebox.showinfo("Info", 'Order not placed.')
   except TypeError as e: #If price is None
       logging.error(f'Item {e} not found in the menu.')
       messagebox.showerror('Error', 'Item not found in the menu.')
       return
   except ValueError as e: #
       logging.error(f'Quantity should be a number: {e}')
       messagebox.showerror('Error', 'Quantity should be a number!')
       return

   conn_menu.close()
   conn_orders.close()

def button_orders_history_click(main_menu_window): #Orders History on Main Menu
    conn = sqlite3.connect('orders_db.db')
    cursor = conn_orders.cursor()
    cursor.execute('SELECT * FROM orders')
    rows = cursor.fetchall()
    conn.close()

    orders_history_window = CTkToplevel()
    orders_history_window.title("Orders History")
    icon = PhotoImage(file='E:\PythonProjects\Restaurant\Restaurant.png')
    orders_history_window.iconphoto(False, icon)
    orders_history_window.geometry('1200x300')

    main_menu_window.withdraw()


    table = ttk.Treeview(orders_history_window, columns=('id','user','item','quantity','sum','date'), show='headings')
    table.pack(padx=10, pady=10, expand=True, fill='both')

    table.heading('id', text='№', anchor='w')
    table.heading('user', text='Name', anchor='w')
    table.heading('item', text='Item', anchor='w')
    table.heading('quantity', text='Quantity', anchor='w')
    table.heading('sum', text='Total', anchor='w')
    table.heading('date', text='Date', anchor='w')
    for row in rows:
        table.insert('','end', values=row)

    scrollbar = ttk.Scrollbar(orders_history_window, orient='vertical', command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    btn_orders_history_back = CTkButton(master=orders_history_window, text='Back', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=lambda:orders_history_back_click(main_menu_window, orders_history_window))
    btn_orders_history_back.pack(padx=20, anchor = 'w')

def orders_history_back_click(main_menu_window, orders_history_window): #Back button on orders history window
    main_menu_window.deiconify()
    orders_history_window.destroy()

def btn_orders_logout_click(home_window, main_menu_window): #Logout button on Main menu
    logout = messagebox.askyesno('Logout', 'Are you sure you want to log out?')
    if logout:
        main_menu_window.destroy()
        home_window.deiconify()
    else:
        pass

#Register Screen
def home_register_button_click(): #Register button on the home screen
    register_window = CTkToplevel()
    register_window.title("Register")
    icon = PhotoImage(file='E:\PythonProjects\Restaurant\Restaurant.png')
    register_window.iconphoto(False, icon)
    register_window.geometry('400x350')
    register_window.resizable(False, False)
    register_window.lift()
    home_window.withdraw()

    register_window_frame = CTkFrame(register_window, width=300, height=200, corner_radius=15)
    register_window_frame.pack(padx=20,pady=20)

    label_register_window = CTkLabel(register_window_frame, text='Registration', font=("Arial",20,'italic'), text_color='#bf2459')
    label_register_window.grid(row=0, column=0, padx=15, pady=10)

    entry_register_username = CTkEntry(master=register_window_frame, placeholder_text='Username...')
    entry_register_username.grid(row=1, column=0, padx=15, pady=10)

    entry_register_password = CTkEntry(master=register_window_frame, placeholder_text='Password...', show='*')
    entry_register_password.grid(row=2, column=0, padx=15, pady=10)

    entry_register_name = CTkEntry(master=register_window_frame, placeholder_text='Name...')
    entry_register_name.grid(row=3, column=0, padx=15, pady=10)

    btn_register = CTkButton(master=register_window_frame, text='Register', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=lambda: btn_register_window_click(entry_register_username, entry_register_password, entry_register_name, register_window))
    btn_register.grid(row=4, column=0, padx=15, pady=10)

    btn_register_cancel = CTkButton(master=register_window_frame, text='Cancel', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=lambda: register_window_cancel_click(home_window, register_window))
    btn_register_cancel.grid(row=5, column=0, padx=15, pady=10)

def btn_register_window_click(entry_register_username, entry_register_password, entry_register_name, register_window): #Register function in register window
    new_username = entry_register_username.get()
    new_password = entry_register_password.get()
    new_name = entry_register_name.get()

    cursor_users.execute("SELECT EXISTS (SELECT 1 FROM users WHERE username = ?);", (new_username,))
    result = cursor_users.fetchone()[0]

    if result:
        messagebox.showwarning("Error", "Username already exists!")
        entry_register_username.delete(0, END)
        entry_register_username.focus_set()
    else:
        sql_insert_newUser = "INSERT OR IGNORE INTO users (username, password, name) VALUES (?, ?, ?)"
        cursor_users.execute(sql_insert_newUser, (new_username, new_password, new_name))
        conn_users.commit()

        sql_insert_existingUser = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor_users.execute(sql_insert_existingUser, (new_username, new_password))
        messagebox.showinfo('Success', 'User registered successfully! You may now log in.')

        register_window.destroy()
        home_window.deiconify()
        conn_users.close()
        btn_place_order_click(new_name,'','')

def register_window_cancel_click(home_window, register_window): #Cancel button on register window
    home_window.deiconify()
    register_window.destroy()

def exit_application():
    exit_app = messagebox.askyesno('Exit', 'Are you sure you want to exit the application?')
    if exit_app:#Exit the application
        home_window.destroy()
        # cursor_users.execute('DELETE FROM users')
        # cursor_users.execute("DELETE FROM sqlite_sequence WHERE name = 'users';")
        # conn_users.commit()
        exit()
    else:
        pass


#Home Window
home_window = CTk()
home_window.title("Restaurant")
home_window.iconbitmap('E:\PythonProjects\Restaurant\Restaurant.ico')
home_window.geometry('400x350')
home_window.resizable(False,False)
home_window._set_appearance_mode('system')


home_window_frame = CTkFrame(home_window, width=300, height=200, corner_radius=10)
home_window_frame.pack(padx=20,pady=20)


app_label=CTkLabel(master=home_window_frame, text="Restaurant", font=("Arial",20,'italic'), text_color='#bf2459')
app_label.grid(row=0, column=0, padx=15, pady=10)

btn_login_home = CTkButton(master=home_window_frame, text="Login", text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=home_login_button_click)
btn_login_home.grid(row=2, column=0, padx=10, pady=10)

btn_register_home = CTkButton(master=home_window_frame, text='Register', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=home_register_button_click)
btn_register_home.grid(row=3, column=0, padx=10, pady=10)

btn_exit_home = CTkButton(master=home_window_frame, text='Exit', text_color='black', fg_color='white', corner_radius=10, hover_color='#bf2459', command=exit_application)
btn_exit_home.grid(row=4, column=0, padx=10, pady=10)

home_window.mainloop()


#Close DB connections
conn_users.close()
conn_menu.close()
conn_orders.close()
