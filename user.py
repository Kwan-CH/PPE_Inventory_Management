import inventory_management
import report_management
import getpass
import jsonParser

config = jsonParser("config.json")
# login purposes
def login():
    attempt = 0
    while attempt < config["maximum_attempt"]: # ensure the log in function is run 3 attempts
        username = input('\nPlease enter your username: ')
        password = getpass.getpass('Please enter your password: ')
        controller_list = []
        lines = report_management.drag_record(config["controller"], 'r', 'low', True) # drag record from controller.txt
        for line in lines:
            name, key = line.split()
            if name == username and key == password:
                print('\nAccess granted\nWelcome to the system, admin')
                return True
        print('\nAccess denied\nPassword or username incorrect, please try again')
        attempt += 1
    return attempt

def register():
    lines = report_management.drag_record(config["controller"], 'r', 'high', False) # drag record from controller.txt
    controller_username = []
    for line in lines:
        controller_username.append(line[0]) # to get the username of every controller
    admin = input('Please enter the admin password to run this action: ') # admin password = 1234
    if admin == config["master_password"] and len(lines) == (config["maximum_accounts"] + 1):
        print('The number of controller for this system is maxed out\nYou cannot perform register action')
        print('Please select another option')
        return False
    elif admin == config["master_password"] and len(lines) < (config["maximum_accounts"] + 1):
        while True:
            username = input('\nEnter a username: ')
            if username in controller_username:# to check whether username input has been taken or not
                print('Username has been taken\nPlease enter a new one')
            else:
                break
        password = input('Enter a password: ').strip()
        print('Account register succesfully, can proceed to log in')
        lines.append([username, password])
        with open('./data/controller.txt', 'w') as file: # insert a new controller record
            for line in lines:
                file.write(f'{line[0]:<10}  {line[1]:<10}\n')
        return True
    else: # if user provide the worng admin password, return back to main body option menu
        print('\nInvalid admin password\nPlease select the option again')
        return False
