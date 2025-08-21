import csv
import time
from selenium import webdriver

for file_path in [
    "C:/Users/HP/Desktop/quantium-starter-repo-main/quantium-starter-repo-main/data/daily_sales_data_0.csv",
    "C:/Users/HP/Desktop/quantium-starter-repo-main/quantium-starter-repo-main/data/daily_sales_data_1.csv",
    "C:/Users/HP/Desktop/quantium-starter-repo-main/quantium-starter-repo-main/data/daily_sales_data_2.csv"
]:
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if(row['product'] == 'pink morsel'):
                Sales = int(row['quantity']) * float(row['price'].replace('$', '').replace(',', ''))
            date = row['date']
            region = row['region']
            print(Sales, date, region)
            with open('output.csv', mode='a', newline='') as output_file:
                fieldnames = ['Sales', 'date', 'region']
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'Sales': Sales, 'date': date, 'region': region})



