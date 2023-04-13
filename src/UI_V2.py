import warnings

from pprint import pprint
from pathlib import Path

import pandas as pd

warnings.simplefilter(action='ignore', category=UserWarning)


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


def get_input(str_to_show):
    print('\n')
    print(str_to_show)
    p = input(' > ').lower()
    p = p.split(',')
    stripped = [s.strip() for s in p]
    for v in stripped.copy():
        match v:
            case 'main' | 'l':
                print(stripped.remove(v))
            case 'h' | 'help':
                print(stripped.remove(v))
    # print(stripped)
    return stripped


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


sensor_items = find_items(main_file)
pprint(sensor_items)
sensors = []
measurements = []
for sensor in sensor_items.keys():
    sensors.append(sensor)
for i in sensor_items.values():
    for item in i:
        measurements.append(item)


def ask_specifics(sensor):
    print('Which data?')
    for item in sensor.items():
        print(f'{item}')


while True:
    data_input = get_input('Welcome.')
    for data in data_input:
        if data in sensor_items.keys():
            ask_specifics(data)
            continue

        match data:
            case 'sensors' | 's':
                print('Sensors:')
                for s in sensors:
                    print(s)
            case 'measurements' | 'm':
                print('Measurements:')
                print(measurements)
            case _:
                print("<ERROR>")
