import os
import glob
import math
import pandas as pd

def extract_and_combine_csv_files(directory, output_file):
    # Search for all .csv files in the specified directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    
    combined_data = {}

    for file in csv_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file)
        
        # Check if the DataFrame has the necessary columns
        if df.shape[1] < 7:
            print(f"File {file} does not have at least seven columns. Skipping.")
            continue
        
        # Process each row in the DataFrame
        for index, row in df.iterrows():
            phone_number = row[1]
            data_to_collect = [row[0], row[4], row[6]]  # Collect 1st, 5th, and 7th columns
            
            if phone_number not in combined_data:
                combined_data[phone_number] = [data_to_collect]
            else:
                combined_data[phone_number].append(data_to_collect)

    # Prepare the consolidated DataFrame
    max_columns = 0
    consolidated_data = {'Phone Number': []}
    for phone_number, data in combined_data.items():
        consolidated_data['Phone Number'].append(phone_number)
        # Flatten the list of lists into a single list for each phone number
        flat_data = [item for sublist in data for item in sublist]
        max_columns = max(max_columns, len(flat_data))
        consolidated_data[phone_number] = flat_data

    # Create a DataFrame with enough columns
    columns = ['رقم الهاتف'] + [f'المحاضرة {math.ceil(i / 3)}' for i in range(max_columns)]
    rows = []
    for phone_number, data in combined_data.items():
        flat_data = [item for sublist in data for item in sublist]
        row = [phone_number] + flat_data + [''] * (max_columns - len(flat_data))
        rows.append(row)
    
    consolidated_df = pd.DataFrame(rows, columns=columns)
    
    # Save the combined DataFrame to a new CSV file
    consolidated_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved as: {output_file}")

if __name__ == "__main__":
    # Specify the directory containing the .csv files
    directory = os.getcwd() + '/files'
    # Specify the output file path
    output_file = os.getcwd() + '/result.csv'
    extract_and_combine_csv_files(directory, output_file)