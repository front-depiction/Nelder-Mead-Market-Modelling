import pandas as pd
import os

# Get a list of all the CSV files in the directory
directory = "/Users/yourusername/Desktop/Market Analysis/Data/"
files = os.listdir(directory)
csv_files = [f for f in files if f.endswith(".csv")]

# Define the start date for the data
start_date = "1983-01-01"

# Create an empty DataFrame to store the resampled data
df_resampled = pd.DataFrame()

# Loop through each CSV file and resample the data to quarters
for file in csv_files:
    filepath = os.path.join(directory, file)
    df = pd.read_csv(filepath)
    df["DATE"] = pd.to_datetime(df["DATE"])  # Convert the "DATE" column to a datetime object
    df = df.set_index("DATE")  # Set the index of the DataFrame to the "DATE" column
    df = df.loc[start_date:]  # Limit the data to years from the start date onwards
    # Convert any non-numeric values to NaN, and then forward-fill the NaN values
    df = pd.to_numeric(df.iloc[:, 0], errors='coerce').ffill()
    df_resampled[file.replace(".csv", "")] = df.resample("M").mean()

# Write the resampled data to a CSV file
output_path = "/Users/yourusername/Desktop/Market Analysis/resampled_data.csv"
df_resampled = df_resampled.fillna(method='ffill')
df_resampled.to_csv(output_path)

# Compare the list of CSV files with the columns in df_resampled
resampled_columns = set(df_resampled.columns)
missing_files = [f for f in csv_files if f.replace(".csv", "") not in resampled_columns]

# Print out any files that were not included in the final resampled data
if missing_files:
    print("The following files were not included in the final resampled data:")
    for file in missing_files:
        print(file)
else:
    print("All files were included in the final resampled data.")