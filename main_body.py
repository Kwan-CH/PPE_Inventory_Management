import user
import jsonParser
import main_menu
import inventory_management

config = jsonParser("config.json")
# drag information from ppe.txt to stand by for checking whether the inventory is initialize or not
file = open(config["ppe"], 'r')
lines = file.readlines()

# drag infromation from controller.txt to stan by for checking whetehr got any admin registered or not (min 1)
file = open(config["controller"], 'r')
controller = file.readlines()

print('\nWelcome to the Health Department PPE Inventory Management System')
while True:
    print('\nPlease select the option')
    choice = input('1) Register\n2) Log in\n3) Exit the system\nOption: ')
    if choice == '1':
        user.register() # user register account
    elif choice == '2':
        if len(controller) < 2: # if no admin
            print('There is no admin yet, please register an admin account')
        else:
            chance = user.login() # user log in
            if chance == 3: # user reached max attempt for log in (max = 3)
                print('You reached the number of attempts to log in')
                break
            else:
                if not bool(lines): # no record at ppe, inventoru is not yet initialized
                    print('\nThe inventory haven\'t created yet, please initialize the inventory')
                    inventory_management.initialize() # inventory initialized fuction
                main_menu.menu() # user logged in, pop option for further action
    elif choice == '3': # user exit system
        print('Thank you for using the system')
        break
    else:
        print('Please enter a valid input') # Error handling for input other than 1, 2, 3