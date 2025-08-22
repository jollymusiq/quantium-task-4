import csv
import os

output_path = "output.csv"

# Clear output file before appending
with open(output_path, mode="w", newline='') as output_file:
    fieldnames = ['Sales', 'date', 'region']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

# Process each input file
for file_name in [
    "../new/data/daily_sales_data_0.csv",
    "../new/data/daily_sales_data_1.csv",
    "../new/data/daily_sales_data_2.csv"
]:
    try:
        with open(file_name, mode="r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['product'] == 'pink morsel':
                    sales = int(row['quantity']) * float(row['price'].replace('$', '').replace(',', ''))
                    date = row['date']
                    region = row['region']
                    print(sales, date, region)

                    with open(output_path, mode="a", newline='') as output_file:
                        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                        writer.writerow({'Sales': sales, 'date': date, 'region': region})
    except FileNotFoundError:
        print(f"File not found: {file_name}")