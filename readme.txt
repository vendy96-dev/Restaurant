This application is built using Python, with the listed modules included:
- sqlite3
- customtkinter
- tkinter
- datetime
- logging


The application creates the local db files when you first start the application.
Note - all the modules, along with python310.dll, database files and the icons are included into the build.


1. Home window - has three buttons - login, register and exit
2. Login window - allows the user to login or create a new account
3. Register window - allows the user to enter a username, password and display name
4. Main menu window - consists of three buttons - new order, order history, and logout
    - new order - allows you to select an item from the dropdown menu, enter the quantity in the textbox, and then place
     your order which will be calculated and displayed to the user in a message box, which asks if the user confirms the order;
    - order history - opens a window with a table with previous orders made
    - logout - logs out the user and opens up the home window
