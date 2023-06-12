import pandas as pd
import tkinter as tk
from dotenv import dotenv_values
from tkinter import font
from tkinter import ttk

env_vars = dotenv_values('.env')
TARGET_ATR_RATIO = float(env_vars['TARGET_ATR_RATIO'])
STOP_LOSS_RATIO = float(env_vars['STOP_LOSS'])
FILE_PATH = env_vars['FILE_PATH']
SHEET_NAME = env_vars['SHEET_NAME']
TARGET_PRICE = None
STOP_LOSS_PRICE = None
NUMBER_OF_SHARES = None
MAXIMUM_RISK = None
COST = None




def read_excel_file(file_path, sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df



def main():
    df = read_excel_file(FILE_PATH, SHEET_NAME)
    print(df.head())

def get_last_id():

    # Read the Excel file into a DataFrame
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

    if df.empty:
        return 1
    else:
        last_id = df['ID'].max()
        return last_id + 1

def filter_stock_prices(stock_name):
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    filtered_df = df[df['Stock Name'] == stock_name]
    prices = filtered_df['Price'].tolist()
    return prices

def get_price_by_id(stock_id):
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    filtered_df = df[df['ID'] == stock_id]
    price = filtered_df['Price'].values[0]
    name = filtered_df['Stock Name'].values[0]
    return price, name

def calculate_target_price():
    atr = float(atr_entry.get())
    price = float(price_entry.get())
    TARGET_PRICE = (atr * TARGET_ATR_RATIO) + price
    return TARGET_PRICE

def calculate_stop_loss():
    price = float(price_entry.get())
    atr = float(atr_entry.get())
    STOP_LOSS_PRICE = ((-1 * atr) * STOP_LOSS_RATIO) + price
    return STOP_LOSS_PRICE

def calculate_number_of_shares():
    equity = float(equity_balance_entry.get())
    risk_percentage = float(risk_on_equity_entry.get())
    atr = float(atr_entry.get())
    NUMBER_OF_SHARES = ((equity * risk_percentage) / 100) / atr
    stock_price = float(price_entry.get())
    total_cost = NUMBER_OF_SHARES * stock_price
    if total_cost > (equity / 4):
        NUMBER_OF_SHARES =  (equity / 4) / stock_price
    
    return NUMBER_OF_SHARES

def calculate_maximum_risk():
    atr = float(atr_entry.get())
    NUMBER_OF_SHARES = calculate_number_of_shares()
    MAXIMUM_RISK = NUMBER_OF_SHARES * atr
    return MAXIMUM_RISK

def calcualte_cost():
    price = float(price_entry.get())
    NUMBER_OF_SHARES = calculate_number_of_shares()
    COST = NUMBER_OF_SHARES * price
    return COST

def calculate():
    target_price_label.configure(text=calculate_target_price())
    stop_loss_label.configure(text = calculate_stop_loss())
    num_shares_label.configure(text = calculate_number_of_shares())
    cost_label.configure(text = calcualte_cost())
    maximum_risk_label.configure(text = calculate_maximum_risk())

def insert_data():
    date_value = entry_date_entry.get()
    stock_name_value = str(stock_name_entry.get())
    price_value = float(price_entry.get())
    atr_value = float(atr_entry.get())
    chart_type_value = str(chart_type_entry.get())
    comment_value = str(entry_comment_entry.get())
    target_ratio_value = float(target_ratio_entry.get())
    equity_balance_value = float(equity_balance_entry.get())
    risk_on_equity_value = float(risk_on_equity_entry.get())
    stop_loss_ration_value = float(stop_loss_ration_entry.get())

     
    # Read the Excel file into a DataFrame
    df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

    # Create a new DataFrame with the data to insert
    id = get_last_id()
    new_data = pd.DataFrame({
        'ID': [id],
        'Entry Date': [date_value],
        'Stock Name': [stock_name_value],
        'Stock Price': [price_value],
        'ATR': [atr_value],
        'Chart Type': [chart_type_value],
        'Comment': [comment_value],
        'Target Ratio': [target_ratio_value],
        'Equity Balance': [equity_balance_value],
        'Risk on Equity (%)': [risk_on_equity_value],
        'Stop Loss Ratio': [stop_loss_ration_value],
        'Target Price': [calculate_target_price()],
        'Stop Loss Price': [calculate_stop_loss()],
        'Number of Shares': [calculate_number_of_shares()],
        'Maximum Risk': [calculate_maximum_risk()],
        'Cost': [calcualte_cost()],
        'Exit Date': [None],
        'Exit Price': [None],
        'Exit Comment': [None],
        'Profit': [None]
    })

    # Append the new data to the existing DataFrame
    df = pd.concat([df, new_data], ignore_index=True)

    # Write the updated DataFrame back to the Excel file
    df.to_excel(FILE_PATH, sheet_name=SHEET_NAME, index=False)
    entry_date_entry.delete(0, tk.END)
    stock_name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    atr_entry.delete(0, tk.END)
    chart_type_entry.delete(0, tk.END)
    entry_comment_entry.delete(0, tk.END)
    target_ratio_entry.delete(0, tk.END)
    target_ratio_entry.insert(0, TARGET_ATR_RATIO)
    equity_balance_entry.delete(0, tk.END)
    risk_on_equity_entry.delete(0, tk.END)
    stop_loss_ration_entry.delete(0, tk.END)
    stop_loss_ration_entry.insert(0, STOP_LOSS_RATIO)

def show_page1():
    notebook.select(page1)

def show_page2():
    notebook.select(page2)

def submit_data():
    # Get the ID entered in the entry field
    id_value = id_entry.get()

    # Get the exit date and exit price entered in the fields
    exit_date_value = exit_date_entry.get()
    exit_price_value = float(exit_price_entry.get())
    exit_comment_value = exit_comment_entry.get()

    # Read the Excel file into a pandas DataFrame
    data = pd.read_excel(FILE_PATH)
    filtered_data = data[data['ID'] == int(id_value)]
    entry_price = float(filtered_data['Stock Price'].values[0])
    number_of_shares = float(filtered_data['Number of Shares'].values[0])
    # Update the corresponding row in the DataFrame with exit date and exit price
    data.loc[data['ID'] == int(id_value), 'Exit Date'] = exit_date_value
    data.loc[data['ID'] == int(id_value), 'Exit Price'] = exit_price_value
    data.loc[data['ID'] == int(id_value), 'Exit Comment'] = exit_comment_value
    data.loc[data['ID'] == int(id_value), 'Profit'] = (exit_price_value - entry_price) * number_of_shares

    exit_date_entry.delete(0, tk.END)
    exit_price_entry.delete(0, tk.END)
    exit_comment_entry.delete(0, tk.END)
    # Write the updated DataFrame back to the Excel file
    data.to_excel(FILE_PATH, index=False)


def fetch_data():
    # Get the ID entered in the entry field
    id_value = id_entry.get()

    # Read the Excel file into a pandas DataFrame
    data = pd.read_excel(FILE_PATH)

    # Filter the data based on the entered ID
    filtered_data = data[data['ID'] == int(id_value)]

    # Display the retrieved data in the labels
    entry_date_label.configure(text="Entry Date: " + str(filtered_data['Entry Date'].values[0]))
    stock_name_label.configure(text="Stock Name: " + str(filtered_data['Stock Name'].values[0]))
    entry_comment_label.configure(text="Entry Comment: " + str(filtered_data['Comment'].values[0]))
    stock_price_label.configure(text = "Stock Price at Entry: " + str(filtered_data['Stock Price'].values[0]))
    target_price_label_exit.configure(text="Target Price:" + str(filtered_data['Target Price'].values[0]))
    # ... continue with other labels and data columns
if __name__ == "__main__":
    print(TARGET_ATR_RATIO * 3)
    # Create the main window
    window = tk.Tk()
    window.title("Data Insertion")
    CUSTOM_FONT = font.Font(size = 12)

    notebook = ttk.Notebook(window)
    notebook.pack(fill=tk.BOTH, expand=True)
    page1 = tk.Frame(notebook)
    notebook.add(page1, text="Sotck Entry")
    page2 = tk.Frame(notebook)
    notebook.add(page2, text="Stock Exit")

    # Entry Date label and entry field
    entry_date_label = tk.Label(page1, text="Entry Date:", font= CUSTOM_FONT)
    entry_date_label.grid(row=0, column=0)
    entry_date_entry = tk.Entry(page1)
    entry_date_entry.grid(row=0, column=1)

    # Stock Name label and entry field
    stock_name_label = tk.Label(page1, text="Stock Name:", font= CUSTOM_FONT)
    stock_name_label.grid(row=1, column=0)
    stock_name_entry = tk.Entry(page1)
    stock_name_entry.grid(row=1, column=1)

    # Stock Price label and entry field
    price_label = tk.Label(page1, text="Stock Price:", font= CUSTOM_FONT)
    price_label.grid(row=2, column=0)
    price_entry = tk.Entry(page1)
    price_entry.grid(row=2, column=1)

    # ATR label and entry field
    atr_label = tk.Label(page1, text="ATR:", font= CUSTOM_FONT)
    atr_label.grid(row=3, column=0)
    atr_entry = tk.Entry(page1)
    atr_entry.grid(row=3, column=1)

    # Chart Type labatrd entry field
    chart_type_label = tk.Label(page1, text="Chart Type:", font= CUSTOM_FONT)
    chart_type_label.grid(row=4, column=0)
    chart_type_entry = tk.Entry(page1)
    chart_type_entry.grid(row=4, column=1)

    # Entry comment label and entry field
    entry_comment_label = tk.Label(page1, text="Comment:", font= CUSTOM_FONT)
    entry_comment_label.grid(row=5, column=0)
    entry_comment_entry = tk.Entry(page1)
    entry_comment_entry.grid(row=5, column=1)

    # Target ratio label and entry field
    target_ratio_label = tk.Label(page1, text="Target Ratio:", font= CUSTOM_FONT)
    target_ratio_label.grid(row=6, column=0)
    target_ratio_entry = tk.Entry(page1)
    target_ratio_entry.grid(row=6, column=1)
    target_ratio_entry.insert(0, TARGET_ATR_RATIO)

    # Equity balance label and entry field
    equity_balance_label = tk.Label(page1, text="Equity Balance:", font= CUSTOM_FONT)
    equity_balance_label.grid(row=7, column=0)
    equity_balance_entry = tk.Entry(page1)
    equity_balance_entry.grid(row=7, column=1)

    # Risk on equity label and entry field
    risk_on_equity_label = tk.Label(page1, text="Risk on Equity:", font= CUSTOM_FONT)
    risk_on_equity_label.grid(row=8, column=0)
    risk_on_equity_entry = tk.Entry(page1)
    risk_on_equity_entry.grid(row=8, column=1)

    # Stop Loss ratio label and entry field
    stop_loss_ration_label = tk.Label(page1, text="Stop Loss Ratio:", font= CUSTOM_FONT)
    stop_loss_ration_label.grid(row=9, column=0)
    stop_loss_ration_entry = tk.Entry(page1)
    stop_loss_ration_entry.grid(row=9, column=1)
    stop_loss_ration_entry.insert(0, STOP_LOSS_RATIO)

    # Target price label and output field 
    target_price_label = tk.Label(page1, text="Target Price:", font= CUSTOM_FONT)
    target_price_label.grid(row=0, column=2)
    target_price_label = tk.Label(page1, text=TARGET_PRICE)
    target_price_label.grid(row=0, column=3)

    # Stop loss label and output field 
    stop_loss_label = tk.Label(page1, text="Stop Loss Price:", font= CUSTOM_FONT)
    stop_loss_label.grid(row=1, column=2)
    stop_loss_label = tk.Label(page1, text=STOP_LOSS_PRICE)
    stop_loss_label.grid(row=1, column=3)

    # Number of shares label and output field 
    num_shares_label = tk.Label(page1, text="Number of Shares:", font= CUSTOM_FONT)
    num_shares_label.grid(row=2, column=2)
    num_shares_label = tk.Label(page1, text=NUMBER_OF_SHARES)
    num_shares_label.grid(row=2, column=3)

    # Maximum risk label and output field 
    maximum_risk_label = tk.Label(page1, text="Maximum Risk:", font= CUSTOM_FONT)
    maximum_risk_label.grid(row=3, column=2)
    maximum_risk_label = tk.Label(page1, text=MAXIMUM_RISK)
    maximum_risk_label.grid(row=3, column=3)

    # Cost label and output field 
    cost_label = tk.Label(page1, text="Cost:", font= CUSTOM_FONT)
    cost_label.grid(row=4, column=2)
    cost_label = tk.Label(page1, text=COST)
    cost_label.grid(row=4, column=3)

    # Submit button
    submit_button = tk.Button(page1, text="Calculate", command=calculate, font= CUSTOM_FONT)
    submit_button.grid(row=10, columnspan=2, column= 0)

    # Calculate button
    calculate = tk.Button(page1, text="Submit", command=insert_data, font= CUSTOM_FONT)
    calculate.grid(row=10, columnspan=2, column=2)

    id_label = tk.Label(page2, text="Stock ID:", font= CUSTOM_FONT)
    id_label.grid(row=0, column=0)
    id_entry = tk.Entry(page2)
    id_entry.grid(row=0, column=1)
    # Fetch button
    fetch_button = tk.Button(page2, text="Fetch Data", command=fetch_data, font= CUSTOM_FONT)
    fetch_button.grid(row=0, columnspan=2, column=2)
    # Labels to display the retrieved data
    entry_date_label = tk.Label(page2, text="Entry Date:", font= CUSTOM_FONT)
    entry_date_label.grid(row=1, columnspan=1)
    stock_name_label = tk.Label(page2, text="Stock Name:", font= CUSTOM_FONT)
    stock_name_label.grid(row=2, columnspan=1)
    entry_comment_label = tk.Label(page2, text="Entry Comment:", font= CUSTOM_FONT)
    entry_comment_label.grid(row=3, columnspan=1)
    stock_price_label = tk.Label(page2, text="Stock Price at Entry:", font=CUSTOM_FONT)
    stock_price_label.grid(row=4, columnspan=1)
    target_price_label_exit = tk.Label(page2, text="Target Price:", font=CUSTOM_FONT)
    target_price_label_exit.grid(row=5, columnspan=1)
    # Exit Date field
    exit_date_label = tk.Label(page2, text="Exit Date:", font= CUSTOM_FONT)
    exit_date_label.grid(row=6, column=0)
    exit_date_entry = tk.Entry(page2)
    exit_date_entry.grid(row=6, column=1)
    # Exit Price field
    exit_price_label = tk.Label(page2, text="Exit Price:", font= CUSTOM_FONT)
    exit_price_label.grid(row=7, column=0)
    exit_price_entry = tk.Entry(page2)
    exit_price_entry.grid(row=7, column=1)

    exit_comment_label = tk.Label(page2, text="Exit Comment:", font= CUSTOM_FONT)
    exit_comment_label.grid(row=8, column=0)
    exit_comment_entry = tk.Entry(page2)
    exit_comment_entry.grid(row=8, column=1)
    # Submit button
    submit_button = tk.Button(page2, text="Submit", command=submit_data, font= CUSTOM_FONT)
    submit_button.grid(row=9, columnspan=3)
    # Start the GUI event loop
    window.mainloop()