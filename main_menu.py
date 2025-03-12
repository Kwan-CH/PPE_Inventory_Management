
import report_management
import inventory_management

import jsonParser
config = jsonParser("config.json")


def update_supplier_hospitals_file(name, supplier_hospital_list):
    with open(name, 'w') as file:  # write the modification back to the selected txt file
        file.write(f'{f"{name.capitalize()}_Code":<15}   {f"{name.capitalize()}_Name":>25}\n')  # for alignment purposes
        for line in supplier_hospital_list:
            file.write(f'{line[0]:<15}   {line[1]:>25}\n')  # for alignment purposes
    print('\nHere is the new list of the supplier name:')  # print the updated supplier/hospotal list for better reference
    for idx, name in enumerate(supplier_hospital_list):
        print(f'{idx + 1}) {name[-1]}')

def update_supplier(): # update suppliers details, name
    supplier = report_management.drag_record(config["suppliers"], 'r', 'high', True)
    while True:
        print('\nHere is the list of the supplier name:')
        for idx, company in enumerate(supplier):
            print(f'{idx + 1}) {company[-1]}')
        try:
            choice = int(input('Which supplier you want to change: '))
            if 0 < choice < len(supplier) + 1:
                print('\n*Please replace the whitespace in the name with underscore')
                supplier[int(choice) - 1][-1] = input('What is the name of the new supplier: ')
                update_supplier_hospitals_file('suppliers.txt', supplier)
                continue_modify = input('\nDo you want to continue updating suppliers (yes/no): ').lower() # prompt user to continue the update section or not
                if continue_modify == 'no':
                    break
            else:
                print('Please enter a valid input') # error handling for the numeric range
        except ValueError:
            print('Please enter a valid input') # error handling for unexpected data type input

def update_hospital(): # update suppliers details, name
    hospitals = report_management.drag_record(config["hospitals"], 'r', 'high', True)
    while True:
        print('\nHere is the list of the hospital name:')
        for idx, hospital in enumerate(hospitals):
            print(f'{idx + 1}) {hospital[-1]}')
        try:
            choice = int(input('Which hospital you want to change: '))
            if 0 < choice < len(hospitals) + 1:
                print('\n*Please replace the whitespace in the name with underscore')
                hospitals[choice - 1][-1] = input('What is the name of the new hospital: ')
                update_supplier_hospitals_file(config["hospitals"], hospitals)
                continue_modify = input('\nDo you want to continue updating hospitals (yes/no): ').lower() # prompt user to continue the update section or not
                if continue_modify == 'no':
                    break
            else:
                print('Please enter a valid input') # error handling for the numeric range
        except ValueError:
            print('Please enter a valid input') # error handling for unexpected data type input

def menu(): # after successful log in, it will print the option of a controller can do
    while True:
        choice = input('\nPlease select the option:\n1) Received item\n2) Distribute item\n3) Update supplier details\n4) Update hospital details\n5) Generate report\n6) Log out\nOption: ')
        if choice == '1': # received supplies from supplier
            lines = report_management.drag_record(config["ppe"], 'r', 'high', False)
            inventory_management.receive_distribute(lines, 'receive', 1)
        elif choice == '2': # distribute supplies to hospitals
            lines = report_management.drag_record(config["ppe"], 'r', 'high', False)
            inventory_management.receive_distribute(lines, 'distribute', -1)
        elif choice == '3': # update supppliers details, name
            update_supplier()
        elif choice == '4': # update hospitals details, name
            update_hospital()
        elif choice == '5': # generate report, will go different function for more specifc report type
            report_management.report_type()
        elif choice == '6': # log out the controller account, and return back to main body option menu
            print('Logging out...')
            break
        else:
            print('Enter a valid input') # Error handling for input other than 1, 2, 3, 4, 5, 6