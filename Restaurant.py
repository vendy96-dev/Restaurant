from colorama import Fore, Back, Style

#Variables
price = 0
total = 0
newPrice = 0
numberOfOrders = 0
newTotal = 0
oldItemChoice = ""
oldItemNumberOfOrders = 0
welcomedGuests = ['admin']
menu = ['Water', '- 1 BGN,', 'Coffee', '- 0.8 BGN,', 'Tea', '- 0.5 BGN,', 'Beer', '- 1.5 BGN,', 'Soda', '- 1.2 BGN,']

print("Hello. Welcome to our coffee shop!")
#Register
account = input('Do you have a registration? (Y)es, log me in or (N)o, let me create one:\n')
if account.casefold() == 'n':
    newUser = input('Enter username:\n')
    welcomedGuests.append(newUser)
    print(Fore.YELLOW + f"Account {newUser} created! You may now log in.")
    print(Fore.RESET)
elif account.casefold() == 'y':
    print('Proceeding...')
else:
    print(Fore.RED + "That is not a valid option! Aborting...")
    exit()
#Login
name = input('Login:\n')

if name not in welcomedGuests:
    print(Fore.RED + f"No account {name} found. Aborting...")
else:
#Continue with order

    print('Hello, ' + name + ". Welcome to our restaurant. Here is our menu: ")
    print(*menu)
    order = input('What would you like to order?\n')
    if order == "" or order.isdigit():
        print(Fore.RED + "Order must be a text and not be blank! Aborting...")
        exit()
    while order not in menu:
    #if order not in menu:
        addNew = input('We do not have that in our menu. Would you like to add it? (Y)es or (N)o:\n')
        if addNew.casefold() == 'n':
            print(*menu)
            oldItemChoice = input('Please choose another item of the available ones from our menu:\n')
            if oldItemChoice not in menu:
                print(Fore.RED + 'Your order will be cancelled. We are sorry for the inconvenience!')
                exit()
            oldItemNumberOfOrders = input(f'How many {oldItemChoice}s would you like to order?\n')
            if oldItemNumberOfOrders.isascii() or oldItemNumberOfOrders == "":
                print(Fore.RED + 'Number of items should be a digit and not be blank! Aborting...')
                exit()
            if oldItemChoice.casefold() == 'water':
                price = 1
                total = price * float(oldItemNumberOfOrders).__round__(2)
                print(f'You chose {oldItemNumberOfOrders} {menu[0]}s. Your price is {total} BGN.')
            elif oldItemChoice.casefold() == 'coffee':
                price = 0.8
                total = price * float(oldItemNumberOfOrders).__round__(2)
                print(f'You chose {oldItemNumberOfOrders} {menu[2]}s. Your price is {total} BGN.')
            elif oldItemChoice.casefold() == 'tea':
                price = 0.5
                total = price * float(oldItemNumberOfOrders).__round__(2)
                print(f'You chose {oldItemNumberOfOrders} {menu[4]}s. Your price is {total} BGN.')
            elif oldItemChoice.casefold() == 'beer':
                price = 1.5
                total = price * float(oldItemNumberOfOrders).__round__(2)
                print(f'You chose {oldItemNumberOfOrders} {menu[6]}s. Your price is {total} BGN.')
            elif oldItemChoice.casefold() == 'soda':
                price = 1.2
                total = price * float(oldItemNumberOfOrders).__round__(2)
                print(f'You chose {oldItemNumberOfOrders} {menu[8]}s. Your price is {total} BGN.')
            menu.append(order)
            input()
            exit()
        elif addNew.casefold() == "y":
            print(f"What would the price of {order} be?")
            newPrice = input()
            if newPrice == "":
                print(Fore.RED + 'Price cannot be blank! Aborting...')
                exit()
            addItem = "- " + newPrice + " BGN"
            menu.extend([order,addItem])
            print(Fore.RED + 'Our updated menu now includes: ')
            print(*menu)
            print(Fore.RESET)
            numberOfOrders = input(f'How many {order}s would you like to order?\n')
            if numberOfOrders.isascii() or numberOfOrders == "":
                print(Fore.RED + 'Number of items should be a digit and not be blank! Aborting...')
                exit()
            newTotal = float(newPrice.strip(" - BGN")) * float(numberOfOrders)
            print(f'Great! Your total for {numberOfOrders} {order}s is {newTotal} BGN.')
            input()
            exit()
        else:
            print(Fore.RED + "That is not a valid option! Aborting...")
            exit()
    oldItemNumberOfOrders = input(f'How many {order}s would you like to order?\n')
    if oldItemNumberOfOrders.isascii() or oldItemNumberOfOrders == "":
        print(Fore.RED + 'Number of items should be a digit and not be blank! Aborting...')
        exit()
    if order.casefold() == 'water':
                 price = 1
                 total = price * float(oldItemNumberOfOrders).__round__(2)
                 print(f'You chose {oldItemNumberOfOrders} {menu[0]}s. Your price is {total} BGN.')
    elif order.casefold() == 'coffee':
                 price = 0.8
                 total = price * float(oldItemNumberOfOrders).__round__(2)
                 print(f'You chose {oldItemNumberOfOrders} {menu[2]}s. Your price is {total} BGN.')
    elif order.casefold() == 'tea':
                 price = 0.5
                 total = price * float(oldItemNumberOfOrders).__round__(2)
                 print(f'You chose {oldItemNumberOfOrders} {menu[4]}s. Your price is {total} BGN.')
    elif order.casefold() == 'beer':
                 price = 1.5
                 total = price * float(oldItemNumberOfOrders).__round__(2)
                 print(f'You chose {oldItemNumberOfOrders} {menu[6]}s. Your price is {total} BGN.')
    elif order.casefold() == 'soda':
                 price = 1.2
                 total = price * float(oldItemNumberOfOrders).__round__(2)
                 print(f'You chose {oldItemNumberOfOrders} {menu[8]}s. Your price is {total} BGN.')
    else:
        print(Fore.RED + "That is not a valid option! Aborting...")
        exit()
    input()














