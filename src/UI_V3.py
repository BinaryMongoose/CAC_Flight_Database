import warnings
import itertools
from pathlib import Path
from pprint import pprint

import pandas as pd
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=UserWarning)

sensor_items = {}

intro_text = """\
We have made a payload with four major sensors.
You can navigate this database by searching for:
 - Data type
 - Sensor name.
 - Position of sensor.
          
Type "h" or "help" for more information. Otherwise, I'll assume you know what you are doing."""

help_text = """\
Box Diagram:
+------------------------+-------------------+
|          OUT           |        IN         |
+------------------------+-------------------+
| LTR (UV)               |                   |
| BME (temp & alt)       | ISM (acc x, y, z) |
| GPS (cord, speed, alt) |                   |
+------------------------+-------------------+
"""


def user_help(h_input):
    print(help_text)


def specify_mes(item):
    m_items = []
    m_input = get_input(f'Based on {item}, what measurement do you want?\n'
                        f'Available Measurements:\n'
                        f'{sensor_items[item]}')
    for m in m_input:
        if m in sensor_items[item]:
            m_items.append(f'{item}_{m}')
        else:
            print(f'{item} does not exist.')

    return m_items


def specify_sensors(item):
    s_items = []
    a_sensors = []
    for sensor in sensor_items.keys():
        if item in sensor_items[sensor]:
            a_sensors.append(sensor)

    s_input = get_input(f'Based on {item}, what sensor data do you want?\n'
                        f'Available Sensors:\n'
                        f'{a_sensors}')

    for s in s_input:
        if s in a_sensors:
            s_items.append(f'{s}_{item}')
        else:
            print(f'{item} does not exist.')

    return s_items


def visualize(v_input):
    header = main_file.columns
    graph_data = []

    if not v_input:  # Checking if we got anything from advanced users.
        v_input = get_input(' [-] Visualize [-] ')
    for item in v_input:
        for sensor, m in sensor_items.items():
            if item == sensor:
                graph_data.append(specify_mes(item))
            elif item in m:
                graph_data.append(specify_sensors(item))
        if item in header:
            graph_data.append(item)

    graph_data = list(itertools.chain(*graph_data))

    if graph_data:
        graph = main_file[graph_data]
        graph.plot()
        plt.show()


def get_input(str_to_show=''):
    # Actually slicing and dicing the string to match specs.
    print('\n')
    print(str_to_show)
    p = input('--> ').lower()
    p = p.split(',')
    stripped = [s.strip() for s in p]
    for i, v in enumerate(stripped):
        stripped[i] = v.replace(' ', '_')
        stripped[i] = v.replace('-', '_')
        stripped[i] = v.replace('altitude', '_')
        stripped[i] = v.replace('temperature', '_')

    # Should move to another function, but can't be bothered.
    match stripped:
        case ('h', *h_input):
            user_help(h_input)
        case ('v', *v_input):
            visualize(v_input)
    return stripped


def load_file(path_to_file):
    home_path = Path(__file__).resolve()

    # You need to make this path not relative.
    path = home_path.parents[1] / Path(path_to_file)

    # Also storing the file as a panda object.
    flight_panda = pd.read_csv(path)

    try:
        flight_panda['hh.mm'] = pd.to_datetime(flight_panda['gps_time'])
    except:
        # I know this is bad! But I can't have this exception slowing the program down.
        flight_panda['hh.mm'] = pd.to_datetime(flight_panda['eye_time'])
    flight_panda['hh.mm'] = flight_panda['hh.mm'].dt.strftime('%H:%M')
    flight_panda = flight_panda.set_index('hh.mm')

    return flight_panda


main_file = load_file('src/formatted_data2.csv')


def find_items(file):
    sensor_items = {}
    header = list(file.columns)
    for column_name in header:
        sep_index = column_name.find('_')
        if sep_index == -1:
            print(f'{column_name} does not have any items.')
            continue
        sensor = column_name[:sep_index]
        sensor_items[sensor] = []
    for column_name in header:
        sep_index = column_name.find('_')
        if sep_index == -1:
            print(f'{column_name} does not have any items.')
            continue
        sensor = column_name[:sep_index]
        item = column_name[sep_index + 1:]
        sensor_items[sensor].append(item)
    return sensor_items


def intro():
    # Only shows up once. Makes everything run.
    global sensor_items
    sensor_items = find_items(main_file)
    print(intro_text)
    while True:
        get_input(' [-] Main [-] ')


intro()
