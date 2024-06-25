import csv

with open('test.csv', 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        print({row['id']:row})
        break
