from datetime import datetime
date_format="%d-%m-%Y"
CATEGORIES={"I":"Income","E":"Expense"}
def get_date(promt,allow_default=False):# here allow default handles if the date is not entered it taked current date automatically
    date_str=input(promt)
    if allow_default is True and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date=datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid Date Format. Please Enter Date in dd-mm-yyyy Format ")
        return get_date(promt,allow_default)
    
def get_amount():
    try:
        amount=float(input("Enter the Amount: "))
        if amount<=0:
            raise ValueError("Amount must be  non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    
def get_category():
    category=input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid Category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()

def get_description():
    return input("Enter a Description (Optional): ")
    

