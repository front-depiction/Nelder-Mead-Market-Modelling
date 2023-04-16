import pandas as pd
from fredapi import Fred
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

output_path = "/Users/yourusername/Desktop/Market Analysis/resampled_data.csv"

popular_indicators = sorted([
    ("DEXCAUS", "Canada / U.S. Foreign Exchange Rate"),
    ("A191RL1Q225SBEA", "Real Gross Domestic Product"),
    ("CPIAUCSL", "Consumer Price Index for All Urban Consumers"),
    ("CPILFESL", "Consumer Price Index for All Urban Consumers: All Items Less Food & Energy"),
    ("M1SL", "M1 Money Stock"),
    ("M2SL", "M2 Money Stock"),
    ("T10Y2Y", "10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity"),
    ("UNRATE", "Unemployment Rate"),
    ("ICSA", "Initial Claims"),
], key=lambda x: x[1])

def resample_fred_data(api_key, series_ids, start_date, end_date, time_interval):
    fred = Fred(api_key=api_key)
    t_frame = time_interval.upper()

    # Validate the time interval
    if t_frame not in ['W', 'M', 'Q']:
        raise ValueError("Invalid time interval. Allowed values are 'W', 'M', or 'Q'.")

    # Create an empty DataFrame to store the resampled data
    df_resampled = pd.DataFrame()

    # Loop through each FRED series ID and resample the data to the specified time unit
    for series_id in series_ids:
        try:
            df = pd.DataFrame(fred.get_series(series_id, start_date, end_date))
        except ValueError as e:
            print(f"Error for {series_id}: {e}")
            continue
        
        df.index.name = "DATE"
        df.columns = [series_id]
        # Convert any non-numeric values to NaN, and then forward-fill the NaN values
        df = pd.to_numeric(df.iloc[:, 0], errors='coerce').ffill()
        df_resampled[series_id] = df.resample(t_frame).mean()

    # Write the resampled data to a CSV file
    output_path = output_path_var.get()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_resampled = df_resampled.fillna(method='ffill')
    df_resampled.to_csv(output_path)

    print("All files were included in the final resampled data.")

# Set the default indicators (using their codes) here
default_indicators = ["UNRATE", "CPIAUCSL", "GDP", "FEDFUNDS", "PAYEMS"]

start_date = '2000-01-01'
end_date = '2021-01-01'
time_interval = 'M'

bottom_frame = tk.Tk()
bottom_frame.title("FRED Data Resampler")

bottom_frame.columnconfigure(0, weight=1)

top_frame = tk.Frame(bottom_frame)
top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
top_frame.columnconfigure(0, weight=0)
top_frame.columnconfigure(1, weight=1)

api_key_var = tk.StringVar(value='6fcfd7e4aa7dc78d6e9635ed058d3fc4')
start_date_var = tk.StringVar(value=start_date)
end_date_var = tk.StringVar(value=end_date)
time_interval_var = tk.StringVar(value=time_interval)

api_key_label = tk.Label(bottom_frame, text="API Key:")
api_key_entry = tk.Entry(bottom_frame, textvariable=api_key_var)
start_date_label = tk.Label(bottom_frame, text="Start Date:")
start_date_entry = tk.Entry(bottom_frame, textvariable=start_date_var)
end_date_label = tk.Label(bottom_frame, text="End Date:")
end_date_entry = tk.Entry(bottom_frame, textvariable=end_date_var)
time_interval_label = tk.Label(bottom_frame, text="Time Interval:")
time_interval_combobox = ttk.Combobox(bottom_frame, textvariable=time_interval_var, values=['W', 'M', 'Q'])
output_path_var = tk.StringVar(value=output_path)

output_path_label = tk.Label(bottom_frame, text="Output Path:")
output_path_entry = tk.Entry(bottom_frame, textvariable=output_path_var)

output_path_label.grid(in_=top_frame, row=4, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
output_path_entry.grid(in_=top_frame, row=4, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")

api_key_label.grid(in_=top_frame, row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
api_key_entry.grid(in_=top_frame, row=0, column=1, padx=(0, 10), pady=(10, 5), sticky="ew")
start_date_label.grid(in_=top_frame, row=1, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
start_date_entry.grid(in_=top_frame, row=1, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")
end_date_label.grid(in_=top_frame, row=2, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
end_date_entry.grid(in_=top_frame, row=2, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")
time_interval_label.grid(in_=top_frame, row=3, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
time_interval_combobox.grid(in_=top_frame, row=3, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")





popular_label = tk.Label(bottom_frame, text="Popular Indicators:")
popular_label.grid(row=4, column=0, padx=(10, 10), pady=(5, 0), sticky="w")

selected_treeview = ttk.Treeview(bottom_frame, selectmode=tk.EXTENDED)

selected_label = tk.Label(bottom_frame, text=f"Selected Indicators: {len(selected_treeview.get_children())}")
selected_label.grid(row=6, column=0, padx=(10, 10), pady=(5, 0), sticky="w")

selected_treeview["columns"] = ("code", "desc")
selected_treeview["show"] = "headings"
selected_treeview.column("code", width=100, anchor="w")
selected_treeview.column("desc", width=400, anchor="w")
selected_treeview.heading("code", text="Code")
selected_treeview.heading("desc", text="Description")

selected_treeview.grid(row=7, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

indicator_treeview = ttk.Treeview(bottom_frame, selectmode=tk.EXTENDED)
indicator_treeview["columns"] = ("code", "desc")
indicator_treeview["show"] = "headings"
indicator_treeview.column("code", width=100, anchor="w")
indicator_treeview.column("desc", width=400, anchor="w")
indicator_treeview.heading("code", text="Code")
indicator_treeview.heading("desc", text="Description")

for code, desc in popular_indicators:
    indicator_treeview.insert("", tk.END, values=(code, desc))
    if code in default_indicators:
        iid = indicator_treeview.focus()
        indicator_treeview.selection_add(iid)

indicator_treeview.grid(row=5, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew")

fred = Fred(api_key=api_key_var.get())

def on_add_manual_indicator():
    new_code = manual_code_var.get()
    if not new_code:
        messagebox.showerror("Error", "Please enter an indicator code.")
        return

    # Check if the input is alphanumeric and not longer than 25 characters
    if not new_code.isalnum() or len(new_code) > 25:
        messagebox.showerror("Error", "Invalid series_id. Series IDs should be 25 or less alphanumeric characters.")
        return

    try:
        # Check if the indicator already exists in the indicator_treeview
        for child in indicator_treeview.get_children():
            if indicator_treeview.item(child)['values'][0] == new_code:
                new_item = indicator_treeview.item(child, "values")
                selected_treeview.insert("", tk.END, values=new_item)
                indicator_treeview.delete(child)
                return
            
        for child in selected_treeview.get_children():
            if selected_treeview.item(child)['values'][0] == new_code:
                messagebox.showwarning("Warning", "The indicator already exists.")
                return

        series_info = fred.get_series_info(new_code)
        new_item = (new_code, series_info.title)
        selected_treeview.insert("", tk.END, values=new_item)

        selected_label.config(text=f"Selected Indicators: {len(selected_treeview.get_children())}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to add the indicator: {e}")



def on_double_click(event, source_treeview, target_treeview):
    item_id = source_treeview.identify_row(event.y)
    if item_id:
        item_values = source_treeview.item(item_id, "values")
        target_treeview.insert("", "end", values=item_values)
        source_treeview.delete(item_id)
    selected_label.config(text=f"Selected Indicators: {len(selected_treeview.get_children())}")


indicator_treeview.bind("<Double-1>", lambda event: on_double_click(event, indicator_treeview, selected_treeview))
selected_treeview.bind("<Double-1>", lambda event: on_double_click(event, selected_treeview, indicator_treeview))


manual_code_label = tk.Label(top_frame, text="Manual Code:")
manual_code_var = tk.StringVar()
manual_code_entry = tk.Entry(top_frame, textvariable=manual_code_var)
manual_code_button = tk.Button(top_frame, text="Add", command=on_add_manual_indicator)

manual_code_label.grid(row=8, column=0, padx=(10, 5), pady=(10, 5), sticky="w")
manual_code_entry.grid(row=8, column=1, padx=(0, 5), pady=(10, 5), sticky="ew")
manual_code_button.grid(row=8, column=2, padx=(5, 10), pady=(10, 5), sticky="ew")


def on_submit():
    api_key = api_key_var.get()
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    time_interval = time_interval_var.get()
    selected_indicators = [indicator_treeview.item(i)["values"][0] for i in indicator_treeview.selection()] + \
                          [selected_treeview.item(i)["values"][0] for i in selected_treeview.get_children()]

    if not api_key or not start_date or not end_date or not time_interval or not selected_indicators:
        messagebox.showerror("Error", "Please fill in all fields and select at least one indicator.")
        return

    try:
        resample_fred_data(api_key, selected_indicators, start_date, end_date, time_interval)
        messagebox.showinfo("Success", f"Data saved at {output_path_var.get()} ")
    except Exception as e:
        messagebox.showerror("Error", str(e))

submit_button = tk.Button(bottom_frame, text="Submit", command=on_submit)
submit_button.grid(row=9, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="ew")

bottom_frame.rowconfigure(5, weight=1)
bottom_frame.mainloop()
