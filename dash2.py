import pandas as pd
import os
from datetime import datetime, timedelta
import time

def merge_csv_files(input_folder_tilt, output_file_tilt):
    # Create an empty DataFrame to store merged data
    merged_data = pd.DataFrame()

    # Iterate through each file in the input folder
    for file_name in os.listdir(input_folder_tilt):
        if file_name.endswith('.csv') and ('DG1' in file_name or 'DG2' in file_name or 'DG3' in file_name):
            file_path = os.path.join(input_folder_tilt, file_name)
            # Read each CSV file into a DataFrame
            data = pd.read_csv(file_path)
            # Merge based on date and time
            merged_data = pd.concat([merged_data, data], ignore_index=True)
            print("Merged tilt file:", file_name)

    # Merge rows with the same date and time
    merged_data = merged_data.groupby(['Date Time (UTC+08:00)']).sum().reset_index()

    # Write the merged DataFrame to a new CSV file
    merged_data.to_csv(output_file_tilt, index=False)
    print("Merged tilt files successfully!")


def merge_crack_files(input_folder, output_file):
    # Create an empty DataFrame to store merged data
    merged_data = pd.DataFrame()

    # Iterate through each file in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv') and ('CM01' in file_name or 'CM02' in file_name or 'CM03' in file_name or 'CM04' in file_name):
            file_path = os.path.join(input_folder, file_name)
            # Read each CSV file into a DataFrame
            data = pd.read_csv(file_path)
            # Merge based on date and time
            merged_data = pd.concat([merged_data, data], ignore_index=True)
            print("Merged crack file:", file_name)

    # Merge rows with the same date and time
    merged_data = merged_data.groupby(['Date Time (UTC+08:00)']).sum().reset_index()

    # Write the merged DataFrame to a new CSV file
    merged_data.to_csv(output_file, index=False)
    print("Merged crack files successfully!")


def run_periodic_merge(input_folder_tilt, output_file_tilt, input_folder, output_file, interval_minutes):
    while True:
        # Remove empty and non-CSV files before merging
        remove_empty_and_non_csv_files(input_folder_tilt)
        remove_empty_and_non_csv_files(input_folder)
        
        # Merge CSV files
        merge_csv_files(input_folder_tilt, output_file_tilt)
        merge_crack_files(input_folder, output_file)
        
        print("Waiting for next merge...")
        time.sleep(interval_minutes * 60)  # Convert minutes to seconds for sleep interval


def remove_empty_and_non_csv_files(folder_path):
    # Iterate through each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file is a CSV file
        if file_name.endswith('.csv'):
            # Check if the CSV file is empty
            if os.path.getsize(file_path) == 0:
                # Remove empty CSV file
                os.remove(file_path)
                print(f"Removed empty CSV file: {file_name}")
        else:
            # Remove non-CSV files
            os.remove(file_path)
            print(f"Removed non-CSV file: {file_name}")


# Provide the input folder containing CSV files and the output file name
input_folder_tilt = r'c:\Users\Jatin\Downloads\workstationgeo'
output_file_tilt = r'c:\Users\Jatin\Downloads\works\test_tilts.csv.csv'
input_folder = r'c:\Users\Jatin\Downloads\workstationgeo'
output_file = r'c:\Users\Jatin\Downloads\works\test_cracks.csv.csv'
interval_minutes = 240  # Set the interval for periodic merge in minutes

# Run the periodic merge process
run_periodic_merge(input_folder_tilt, output_file_tilt, input_folder, output_file, interval_minutes)
