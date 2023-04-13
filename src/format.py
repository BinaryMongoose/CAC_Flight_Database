from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd

home_path = Path(__file__).resolve()

# You need to make this path not relative.
path = home_path.parents[1] / Path('data/HB_combined/Combined_RAW.csv')

# Also storing the file as a panda object.
flight_panda = pd.read_csv(path)
# Storing the header of the file.
header = flight_panda.columns

# Convert GPS time to HH:MM.
try:
    flight_panda['hh.mm'] = pd.to_datetime(flight_panda['gps_time'])
except:
    pass  # I know this is bad! But I can't have this exception slowing the program down.
flight_panda['hh.mm'] = flight_panda['hh.mm'].dt.strftime('%H:%M')
flight_panda = flight_panda.set_index('hh.mm')

flight_panda = flight_panda.drop(columns=['time_since_start'])

flight_panda.to_csv('formatted_data.csv')
