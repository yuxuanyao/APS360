import csv
from os import path

with open('./data/legend.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if str(path.isfile('./images/' + row[1])) is False:
                print('image not found for entry')
            if row[2] in (None, ""):
                print("entry is incomplete")
            line_count += 1
    print(f'Processed {line_count} lines.')