import jsonParser

config = jsonParser("config.json")
item_dict = jsonParser("items.json")
lists_of_keys = list(item_dict.keys())

def drag_record(name, action, specification, indent):
    with open(name, action) as file:
        lines = file.readlines()
        if specification == 'low': # drag record from txt file, and return them as a list of string
            if indent:
                return lines[1:] # exclude the title of each txt file
            else:
                return lines
        else: # return the record as nested list
            item_list = []
            for line in lines:
                item_list.append(line.split())
            if indent:
                return item_list[1:] # exclude the title of each txt file
            else:
                return item_list
# update overall transaction
def transaction_update(supplier_hospital, item_code, quantity, date, initialize):
    with open(config["transaction"], 'a') as file:
        if initialize:
            file.write(f'{"From":<17}    {"To":<17}   {"Item_Code":<9}   {"Item_Name":<11}   {"Quantity(Box)":>13}   {"Date":>12}\n')
        if supplier_hospital.startswith('H'):
            file.write(f'{"Health_Department":<17}    {supplier_hospital:<17}   {item_code:<9}\
   {item_dict.get(item_code):<11}   {quantity:>13}   {date:>12}\n')
        else:
            file.write(f'{supplier_hospital:<17}    {"Health_Department":<17}   {item_code:<9}\
   {item_dict.get(item_code):<11}   {quantity:>13}   {date:>12}\n')

def report_type():
    while True:
        try:
            print('\nPlease select the option')
            choice = int(input('1) Available supplies\n2) Supplies that less than 25 boxes\n3) The distribution of a particular item\n4) List of supplies suppliers supplied\n5) List of hospitals with distribution items\n6) Transaction report for specific month\n7) Exit report section\nOption: '))
            if choice == 1:
                ascending()
            elif choice == 2:
                quantity_less_25()
            elif choice == 3:
                particular_distribution()
            elif choice == 4:
                supplies_suppliers_supplied()
            elif choice == 5:
                hospital_supplies()
            elif choice == 6:
                transaction_month()
            elif choice == 7:
                print('Returning back to main menu')
                break
            else:
                print('Invalid input, please try again')
        except ValueError:
            print('Invalid input, please try again')

# show the quantity of all ppe in ascending order
def ascending():
    ordered = []
    alignment = []
    lines = drag_record(config["ppe"], 'r', 'low', True)
    for line in lines:
        supplier, item_code, item, quantity = line.split()
        ordered.append([item_code, item_dict.get(item_code), int(quantity)])
    ordered = sorted(ordered, key= lambda x:x[2])
    with open(config["report"], 'w') as file:
        alignment.append('The list of items that arrange in ascending order by quantity available\n\n')
        alignment.append(f'{"Item_Code":<9}   {"Item_Name":<12}   {"Quantity":>14}\n')
        for item in ordered:
            alignment.append(f'{item[0]:<9}   {item[1]:<12}   {item[2]:>14}\n')
        for line in alignment:
            file.write(line)
        print('Report generated succesfully, please refer to report.txt')

# show the ppe item that has less than 25 box of quantity
def quantity_less_25():
    items = []
    alignment = []
    lines = drag_record(config["ppe"], 'r', 'low', True)
    for line in lines:
        supplier, item_code, item, quantity = line.split()
        if int(quantity) < 25:
            items.append([item_code, item, quantity])
    with open(config["report"], 'w') as file:
        alignment.append('The list of items that have less than 25 boxes of stock\n\n')
        alignment.append(f'{"Item_Code":<9}   {"Item_Name":<12}   {"Quantity":>14}\n')
        for item in items:
            alignment.append(f'{item[0]:<9}   {item[1]:<12}   {item[2]:>14}\n')
        for line in alignment:
            file.write(line)
    print('Report generated succesfully, please refer to report.txt')

# show the prticular distribution of a ppe item, if it distribute to same hospital it will added up
def particular_distribution():
    title = ['From', 'To', 'Item_Code', 'Item_Name', 'Total']
    distribution = []
    total = {}
    alignment = []
    transcation_lines = drag_record(config["transaction"], 'r', 'high', True)
    hospitals = drag_record(config["hospitals"], 'r', 'high', True)
    for line in transcation_lines:
        if line[0] == 'Health_Department':
            distribution.append(line)
    while True:
        chosen_item = input('\nEnter the item code you want to search: ').upper()
        if chosen_item in lists_of_keys:
            break
        else:
            print('Please enter a valid input')
    for line in distribution:
        if line[2] == chosen_item:
            hospital_code = line[1]
            item = line[2]
            quantity = int(line[-2])
            key = (hospital_code, item)
            if key in total:
                total[key] += quantity
            else:
                total[key] = quantity
    alignment.append(f'The list of {item_dict.get(chosen_item)} that had been distributed to\n\n')
    alignment.append(f'{"Hospital_Name":<22}   {"Quantity(Box)":>14}\n')
    for (hospital_code, item), quantity in total.items():
        for hospital in hospitals:
            if hospital_code == hospital[0]:
                alignment.append(f'{hospital[1]:<22}   {quantity:>14}\n')
    with open(config["report"], 'w') as file:
        for line in alignment:
            file.write(line)
    print('Report generated succesfully, please refer to report.txt')

# show the list of supplies supppliers supplied
def supplies_suppliers_supplied():
    supplier = drag_record(config["suppliers"], 'r', 'high', True)
    supplies = drag_record(config["ppe"], 'r', 'high', True)
    items_supplied = {}
    alignment = []
    for company in supplier:
        temp = []
        for item in supplies:
            if company[0] == item[0]:
                temp.append(item_dict[item[1]])
        items_supplied[company[-1]] = ', '.join(temp)
    alignment.append('The list of suppliers with their PPE equipments supplied\n\n')
    for company, supplies in items_supplied.items():
        alignment.append(f'Suppliers: {company}\n')
        alignment.append(f'Supplies: {supplies}\n\n')
    with open(config["report"], 'w') as file:
        for line in alignment:
            file.write(line)
    print('Report generated succesfully, please refer to report.txt')

# show the list od ppe item that a hospital have
def hospital_supplies():
    hospitals = drag_record(config["hospitals"], 'r', 'high', True)
    transaction_line = drag_record(config["transaction"], 'r', 'high', True)
    hospital_item = {}
    for hospital in hospitals:
        amount_per_item = {'HC': 0, 'FS': 0, 'MS': 0, 'GL': 0, 'GW': 0, 'SC': 0}
        hospital_code = hospital[0]
        for line in transaction_line:
            if hospital_code == line[1]:
                item_code = line[2]
                quantity = int(line[-2])
                if item_code in amount_per_item:
                    amount_per_item[item_code] += quantity
            hospital_item[hospital[1]] = amount_per_item
    with open(config["report"], 'w') as file:
        file.write('The list of hospitals with the amount of items distributed\n')
        for hospitals, supplies in hospital_item.items():
            file.write(f'\n{hospitals}\n')
            for item_code, quantity in supplies.items():
                file.write(f'{item_code}: {quantity}\n')
    print('Report generated succesfully, please refer to report.txt')

# shows the transaction record (receive/distribute) for a specific month
def transaction_month():
    chosed_transaction = []
    transaction_line = drag_record(config["transaction"], 'r', 'high', True)
    while True:
        try:
            chosen_year = int(input('\nWhich year of the transaction you want to see: '))
            chosen_month = int(input('Which month of the year transaction you want to see (use number): '))
            for line in transaction_line:
                day, month, year = line[-1].split('-')
                if int(month) == int(chosen_month) and int(year) == int(chosen_year):
                    chosed_transaction.append(line)
            with open(config["report"], 'w') as file:
                file.write(f'This is the list of transaction that you want to see in month {chosen_month} in year {chosen_year}\n\n')
                file.write(f'{"From":<17}    {"To":<17}   {"Item_Code":<9}   {"Item_Name":<11}   {"Quantity(Box)":>13}\n')
                for line in chosed_transaction:
                    file.write(f'{line[0]:<17}   {line[1]:<17}   {line[2]:<9}   {line[3]:<11}   {line[4]:>13}\n')
                break
        except ValueError:
            print('Please enter a valid input')
    print('Report generated successfully, please refer to report.txt')