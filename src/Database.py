""" A python script that organizes the flight data from CAC's payloads.

"""
import csv, sys, os

files = {}
restart_count = 0
    
header_found = False;

filename = '../data/RAW_HB/FILE_0.csv'
with open(filename, newline='') as f:
    reader = csv.reader(f)
    try:
        i = 0
        for row in reader:
            if 'time' in row[0]:
                count = 0
                
                while True:
                    if 'time' in row[0]:
                        break
                    count += 1
                files[i] = count
            i += 1
            

        # print(files)

    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

for index, count in files.items():
    print(f"There are {count} lines in header section {index}")

print(f'FILE_0 has {len(files.values())} headers.')


