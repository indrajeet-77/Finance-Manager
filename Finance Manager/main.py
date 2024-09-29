import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["Date", "Amount", "Category", "Description"]
    FORMAT = "%d-%m-%Y"

    # Initialize a CSV file
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # Creating columns here
            df = pd.DataFrame(columns=cls.COLUMNS)
            # This creates a CSV file
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, Date, Amount, Category, Description):
        # Storing in dictionary
        new_entry = {
            "Date": Date,
            "Amount": Amount,
            "Category": Category,
            "Description": Description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            # Write header if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(new_entry)  # Python automatically handles closing here
        print("Entry Added Successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        # transaction in data frame
        df = pd.read_csv(cls.CSV_FILE)
        # accessing values at date col
        df["Date"] = pd.to_datetime(df["Date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filter_df = df.loc[mask]  # locates all dif rows wich validates mask

        if filter_df.empty:
            print("No Transactions found in the given data range")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} TO {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filter_df.to_string(
                    index=False, formatters={"Date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )
            total_income = filter_df[filter_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filter_df[filter_df["Category"] == "Expense"]["Amount"].sum()
            print("\nSummary: ")
            print(f"Total Income:Rs{total_income:.2f}")
            print(f"Total Expense: Rs{total_expense:.2f}")
            print(f"Total Savings: Rs{total_income-total_expense:.2f}")
            
        return filter_df   

    @classmethod
    def add(cls):
        cls.initialize_csv()
        Date = get_date(
            "Enter the Date of the transaction(dd-mm-yyyy) or press Enter for today's date: ",
            allow_default=True,
        )
        Amount = get_amount()
        Category = get_category()
        Description = get_description()
        cls.add_entry(Date, Amount, Category, Description)
    
    def plot_transactions(df):
        df.set_index("Date",inplace=True)
        
        income_df=(df[df["Category"]=="Income"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
        )
        
        expense_df=(df[df["Category"]=="Expense"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
        )
        plt.figure(figsize=(10,5))
        plt.plot(income_df.index,income_df["Amount"],label="Income",color="g")
        plt.plot(expense_df.index,expense_df["Amount"],label="Expense",color="r")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Income and Expenses over time")
        plt.legend()
        plt.grid(True)
        # shows the pplote
        plt.show()
        


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary with a date range")
        print("3. Exit")
        choice=input("Enter your choice (1-3): ")
        
        if choice=="1":
            CSV.add()
        elif choice=="2":
            start_date=get_date("Entet the start date(dd-mm-yy): ")
            end_date=get_date("Enter the end date (dd-mm-yy): ")
            df= CSV.get_transactions(start_date,end_date)
            if input("DO you want to see a plot? (y/n)").lower()=="y":
                CSV.plot_transactions(df)
                
        elif choice=="3":
            print("Exiting.....")
            print("Exited")
            break
        else:
            print("Enter valif choice (1,2,or 3)")
if __name__=="__main__":
    main()

    
            
            
            
            

