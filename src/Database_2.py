import csv, sys, os
from pprint import pprint

restarts = {}
restart_index = []

true_header = None

filename = '../data/RAW_HB/FILE_0.csv'
with open(filename) as f:
    file = f.readlines()

true_header = file[0]

index = 0
for line in file:
    if line == true_header:
        restart_index.append(index)
        # print(line)
    index += 1

for i in range(0, len(restart_index)):
    print(i)
    try:
        restarts[i] = file[restart_index[i]:restart_index[i + 1]]
    except:
        pass
    
        
    


pprint(restarts)
