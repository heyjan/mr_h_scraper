import csv

# Function to filter THC percentages between 1% and 10%
def filter_thc(thc):
    if thc is None:
        return False
    try:
        thc_percentage = float(thc.strip('%'))  # Remove '%' and convert to float
        return 1 <= thc_percentage <= 10
    except ValueError:
        return False  # Return False for non-numeric THC values

def filter_and_save_data(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, \
            open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            thc = row['THC']
            if filter_thc(thc):
                writer.writerow(row)

# File paths
input_csv = 'full_data.csv'
output_csv = 'filtered_data.csv'

# Filter and save data
filter_and_save_data(input_csv, output_csv)

print("Filtered data has been saved to filtered_data.csv")
