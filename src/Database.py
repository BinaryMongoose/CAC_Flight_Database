""" A python script that organizes the flight data from CAC's payloads.

"""
import csv, sys, os

data_folder = "../data/RAW_HB/"

restart_count = 0

def count_files():
    flight_files = os.listdir(data_folder)
    return len(flight_files)
    

filename = '../data/RAW_HB/FILE_0.csv'
with open(filename, newline='') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            # print(row)
            if 'time' in row[0]:
                restart_count += 1

    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

    print(f"There are {count_files()} files in the folder.")
    print(f"The payload restarted {restart_count} times.")

def parse_file(header, pattern):
    pass    

