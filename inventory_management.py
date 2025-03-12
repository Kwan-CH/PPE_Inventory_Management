import report_management
import jsonParser
config = jsonParser("configs.json")
item_dict = jsonParser("items.json")
lists_of_keys = list(item_dict.keys()) # to get the list of item code

lists_of_hospital = report_management.drag_record(config["hospitals"], 'r', 'high', True)
hospital_code = []
for hospitals in lists_of_hospital: # to get the list of hospital code
    hospital_code.append(hospitals[0])


# prompt user for the supplier code, item code and quantity
def information(action):
    while True:
        try:
            while True:
                item_code = input('\nThe item code: ').upper() # to check the item code input exist or not
                if item_code in lists_of_keys:
                    quantity = int(input(f'The quantity {action}: '))
                    if action.lower() == 'initialize':
                        code = input('The supplier code for the item: ').upper()
                    elif action.lower() == 'receive': # if receive, the item code can act as foreign key to to take suppleir code
                        code = None # so no need to prompt for supplier code
                    elif action.lower() == 'distribute':
                        while True:
                            code = input('The hospital code for the distribution: ').upper() # to check the hospital code input exist or not
                            if code in hospital_code:
                                break
                            else:
                                print('Please enter a valid input\n')
                    date = input(f'What is the date of the item that {action}d (in the form of day-month-year): ')
                    return code, item_code, quantity, date
                else:
                    print('Please enter a valid input') # error handling if teh item code input does not exist
        except:
            print('Please enter a valid input') # error handling for unexpected data type input

def update_inventory(ppe):
    formatted = []
    for line in ppe:
        part = line.split(',')
        alignment = f'{part[0]:<13}   {part[1]:<9}   {part[2]:<13}   {part[3]:>14}' # for alignment purposes
        formatted.append(alignment)
    with open(config["ppe"], 'w') as file: # update the ppe with the modification done
        file.write('\n'.join(formatted) + '\n')

# initialize the inventory / create inventory
def initialize():
    lines = ['Supplier_Code,Item_Code,Item_Name,Quantity(Box)']
    while True:
        try:
            number = int(input('How many items you want to initialize: '))
            for i in range(number):
                suppliers, item_code, quantity, date = information('initialize')
                lines.append(f'{suppliers},{item_code},{item_dict.get(item_code)},{str(quantity)}')
                report_management.transaction_update(suppliers, item_code, quantity, date, (True if i == 0 else False))
                # if i == 0 True for the writing of the title of the file, when iterate again i = 1 no more title to be write again
            update_inventory(lines)
            break
        except ValueError:
            print('Please enter a valid value') # error handling for unexpected data type input

# check for item availability before distribute
def sufficiency(item, quantity):
    amount = quantity
    while True:
        if amount > int(item[-1]):
            print('\nThe item currently now is not sufficient to meet your demands')
            print('Please enter a appropriate value this time')
            print(f'The current availability of the item is {item[-1]}')
            amount = int(input('The amount distribute: '))
        else:
            break
    return amount

# receive or distribute
def receive_distribute(ppe, action, plus_minus_one):
    suppliers_hospital, item_code, quantity, date = information(action)
    supplies = report_management.drag_record(config["ppe"], 'r', 'high', True)
    for idx, item in enumerate(ppe):
        if item_code in item:
            if plus_minus_one == -1:
                quantity = sufficiency(item, quantity)
            item[-1] = str(int(item[-1]) + (quantity * plus_minus_one))
            if suppliers_hospital is None:
                for equipment in supplies:
                    if item_code in equipment:
                        suppliers_hospital = equipment[0]
            report_management.transaction_update(suppliers_hospital, item_code, quantity, date, False)
        ppe[idx] = ', '.join(item)
    update_inventory(ppe)
