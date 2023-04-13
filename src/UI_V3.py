import warnings
from pathlib import Path
from pprint import pprint

import pandas as pd
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=UserWarning)


intro_text = """\
We have made a payload with four major sensors.
You can navigate this database by searching:
 - Data Type
 - Sensor name.
 - Position of sensor.
          
Type "h" or "help" for more information. Otherwise, I'll assume you know what you are doing."""


help_text= """\
Box Diagram:
+------------------------+-------------------+
|          OUT           |        IN         |
+------------------------+-------------------+
| LTR (UV)               |                   |
| BME (temp & alt)       | ISM (acc x, y, z) |
| GPS (cord, speed, alt) |                   |
+------------------------+-------------------+
"""


def load_file(path_to_file):
    home_path = Path(__file__).resolve()

    # You need to make this path not relative.
    path = home_path.parents[1] / Path(path_to_file)

    # Also storing the file as a panda object.
    flight_panda = pd.read_csv(path)

    try:
        flight_panda['hh.mm'] = pd.to_datetime(flight_panda['gps_time'])
    except:
        pass  # I know this is bad! But I can't have this exception slowing the program down.
    flight_panda['hh.mm'] = flight_panda['hh.mm'].dt.strftime('%H:%M')
    flight_panda = flight_panda.set_index('hh.mm')

    return flight_panda


main_file = load_file('src/formatted_data2.csv')


def main():
    print(intro_text)




main()
