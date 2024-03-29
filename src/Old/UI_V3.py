import itertools
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

warnings.simplefilter(action='ignore', category=UserWarning)

sensor_items = {}
sensor_pos = {'inside': ['LTR', 'BME', 'GPS'],
              'outside': ['ISM']}

intro_text = """\
We have made a payload with four major sensors.
You can navigate this database by searching for:
 - Data type
 - Sensor name.
 - Position of sensor.
          
Type "h" or "help" for more information. Otherwise, I'll assume you know what you are doing."""

help_text = f"""\
Box Diagram:
+------------------------+-------------------+
|          OUT           |        IN         |
+------------------------+-------------------+
| LTR (UV)               |                   |
| BME (temp & alt)       | ISM (acc x, y, z) |
| GPS (cord, speed, alt) |                   |
+------------------------+-------------------+

Available Sensors:
{list(sensor_items.keys())}

Available Measurements:


"""


def user_help():
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
            print(f'{m} does not exist.')

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
            print(f'{s} does not exist.')

    return s_items


def get_time():
    time_slice = []
    time_input = get_input('''Visualize - What time frame do you want?
You can choose from 10:31 to 4:41.''')

    for i, time in enumerate(time_input):
        sep_index = time.find(':')
        if sep_index == -1:
            a = int(time[:1])
            b = int(time[1:])

            if a < 9:
                a = f'0{a}'
            if b < 9:
                b = f'0{b}'

            time = f'{a}:{b}'
        elif sep_index == 2:
            time = time
            time_slice.append(time)
            continue
        else:
            a = int(time[0:sep_index])
            b = int(time[sep_index + 1:])
            if a < 9:
                a = f'0{a}'
            if b < 9:
                b = f'0{b}'
            time = f'{a}:{b}'
        time_slice.append(time)

    return time_slice


def generate_legend(graph_data):
    legend = []
    for data in graph_data:
        m_data = data.replace('_', ' ')
        m_data = m_data.replace('ism', 'Inside')
        m_data = m_data.replace('bme', 'Outside')
        legend.append(m_data)

    return legend


def visualize(v_input):
    header = list(main_file.columns)
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
    # is_multi_list = any(isinstance(i, list) for i in graph_data)
    # if is_multi_list:
    graph_data = [item for sublist in graph_data for item in sublist]

    if graph_data:
        graph = main_file[graph_data]
        legend = generate_legend(graph_data)
        print(legend)
        try:
            time_slice = get_time()
            print(time_slice)
            graph = graph[time_slice[0]:time_slice[1]]
        except IndexError as e:
            print(f'{e} occurred, defaulting to interesting time range')
            graph = graph['11:20':'02:30']

        # for data in graph_data:
        #     sub_graph = main_file[data]
        #     sub_graph.plot()

        graph.plot(subplots=True)
        plt.legend()
        plt.show()


def get_input(str_to_show=''):
    new_stripped = []
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
    for v in stripped:
        if v != '':
            new_stripped.append(v)

    # Should move to another function, but can't be bothered.
    match new_stripped:
        case ('h', *h_input):
            user_help()
        case ('v', *v_input):
            visualize(v_input)
    return new_stripped


def load_file(path_to_file):
    home_path = Path(__file__).resolve()

    # You need to make this path not relative.
    path = home_path.parents[1] / Path(path_to_file)

    # Also storing the file as a panda object.
    flight_panda = pd.read_csv(path)

    try:
        flight_panda['hh.mm'] = pd.to_datetime(flight_panda['gps_time'])
    except KeyError:
        # I know this is bad! But I can't have this exception slowing the program down.
        flight_panda['hh.mm'] = pd.to_datetime(flight_panda['eye_time'])
    flight_panda['hh.mm'] = flight_panda['hh.mm'].dt.strftime('%H:%M')
    flight_panda = flight_panda.set_index('hh.mm')

    return flight_panda


main_file = load_file('data/Payload_2.csv')


def find_items(file):
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
        get_input(' [-] Main.py [-] ')


intro()
