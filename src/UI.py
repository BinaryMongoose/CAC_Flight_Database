from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt
import pandas as pd


title = '''
    
██╗  ██╗██╗ ██████╗ ██╗  ██╗         █████╗  ██╗   ████████╗██╗████████╗██╗   ██╗██████╗ ███████╗
██║  ██║██║██╔════╝ ██║  ██║        ██╔══██╗ ██║   ╚══██╔══╝██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
███████║██║██║  ██╗ ███████║        ███████║ ██║      ██║   ██║   ██║   ██║   ██║██║  ██║█████╗  
██╔══██║██║██║  ╚██╗██╔══██║        ██╔══██║ ██║      ██║   ██║   ██║   ██║   ██║██║  ██║██╔══╝  
██║  ██║██║╚██████╔╝██║  ██║        ██║  ██║ ███████╗ ██║   ██║   ██║   ╚██████╔╝██████╔╝███████╗
╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝        ╚═╝  ╚═╝ ╚══════╝ ╚═╝   ╚═╝   ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝
'''


def get_input(str_to_show):
    print('\n\n')
    print(str_to_show)
    p = input(' > ').lower()
    p = p.split(',')
    stripped = [s.strip() for s in p]
    for i, v in enumerate(stripped.copy()):
        stripped[i] = v.replace("data", "")
        stripped[i] = v.replace(" ", "_")
        stripped[i] = v.replace("-", "_")
        stripped[i] = v.replace('altitude', 'alt')
        stripped[i] = v.replace('acceleration', 'acc')
        match v:
            case 'main' | 'm':
                stripped.remove(v)
                main_scene(main_file)
            case 'h' | 'help':
                stripped.remove(v)
                text_help()
            case '':
                stripped.remove(v)
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
        pass  # I know this is bad! But I can't have this exception slowing the program down.
    flight_panda['hh.mm'] = flight_panda['hh.mm'].dt.strftime('%H:%M')
    flight_panda = flight_panda.set_index('hh.mm')

    return flight_panda


main_file = load_file('data/HB_combined/Combined_RAW.csv')


def text_help():
    print('''
    I'm a help section!
    
    Someone still needs to fill me in!''')


# if ('acc' or 'acceleration') in items_to_show:
#     print('Which acceleration data do you want to see?')
#     acc_choice = input('Acceleration X, Y, Z, or All\n> ').lower()
#     acc_choices = acc_choice.split(',')
#     for choice in acc_choices:
#         choice = choice.strip()
#         choice = choice.lower()
#         if choice == 'all':
#             data_present.clear()
#             data_present.append('acc_x')
#             data_present.append('acc_y')
#             data_present.append('acc_z')
#             break
#         elif choice == 'help':
#             help()
#             break
#         else:
#             if f'acc_{choice}' in data_present:
#                 continue
#             elif f'acc_{choice}' not in header:
#                 continue
#             else:
#                 data_present.append(f'acc_{choice}')
#
# if 'gps' in items_to_show:
#     print('What GPS data do you want to see?')
#     gps_choice = input('GPS speed, time, or alt\n> ')
#     gps_choices = gps_choice.split(',')
#     for choice in gps_choices:
#         choice = choice.strip()
#         choice = choice.lower()
#         if choice == 'all':
#             data_present.clear()
#             data_present.append('gps_speed')
#             data_present.append('gps_alt')
#             data_present.append('gps_time')
#             break
#         elif choice == 'help':
#             help()
#             break
#         else:
#             if f'gps_{choice}' in data_present:
#                 continue
#             elif f'gps_{choice}' not in header:
#                 continue
#             else:
#                 data_present.append(f'gps_{choice}')
#

def organize(file):
    pass


def visualize(file):
    header = list(main_file.columns)
    items_to_show = []
    time_slice = []

    while not items_to_show:
        data_input = get_input('Visualize - What data do you want to see?')
        for item in data_input.copy():
            match item:
                case 'alt':
                    alt_choices = get_input('What altitude data do you want?')
                    for choice in alt_choices:
                        match choice:
                            case 'gps':
                                items_to_show.append('gps_alt')
                            case 'bme':
                                items_to_show.append('bme_alt')
                            case 'all':
                                items_to_show.append('gps_alt')
                                items_to_show.append('bme_alt')
                    continue
                case 'gps':
                    gps_choices = get_input('What GPS data do you want?')
                    for choice in gps_choices:
                        match choice:
                            case 'speed':
                                items_to_show.append('speed')
                            case 'alt':
                                items_to_show.append('gps_alt')
                            case 'all':
                                items_to_show.append('speed')
                                items_to_show.append('gps_alt')
                    continue
                case 'acc':
                    acc_choices = get_input('What acceleration data do you want?')
                    for choice in acc_choices:
                        match choice:
                            case 'x':
                                items_to_show.append('acc_x')
                            case 'y':
                                items_to_show.append('acc_y')
                            case 'z':
                                items_to_show.append('acc_z')
                            case 'all':
                                items_to_show.append('acc_x')
                                items_to_show.append('acc_y')
                                items_to_show.append('acc_z')
                    continue
            print(items_to_show)
            if (item in header) and (item not in items_to_show):
                items_to_show.append(item)
            elif item not in header:
                print(f'{item} does not exist.')

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

            time_input[i] = f'{a}:{b}'
        elif sep_index == 2:
            time_input[i] = time
            continue
        else:
            a = int(time[0:sep_index])
            b = int(time[sep_index + 1:])
            if a < 9:
                a = f'0{a}'
            if b < 9:
                b = f'0{b}'
            time_input[i] = f'{a}:{b}'
        time_slice.append(time)

    print(time_slice)
    graph = main_file[items_to_show]
    try:
        graph = graph[time_slice[0]:time_slice[1]]
    except IndexError:
        print('Error occurred, defaulting to whole time range')

    # Display data.
    if not graph.empty:
        graph.plot()
        plt.show()


def store(file):
    pass


def main_scene(file):
    while True:
        user_inputs = get_input('What do you want to do?')
        mainScene_input = user_inputs[0]

        match mainScene_input:
            case 'organize' | 'o':
                organize(file)
            case 'visualize' | 'v':
                visualize(main_file)
            case 'store' | 's':
                store(main_file)
            case _:
                print(f"I'm sorry I can't {mainScene_input}.")
                continue


# print(''' ----------+ Flight Database +----------
# Hello! Welcome to CAC Flight Database. I'm here to help you
# organize, visualize, and store the data from CAC's high altitude balloon launch.
#
# If you need to send multiple commands remember to use commas. Spaces are not accepted
# as delimiters. ''')
#
#
# # Ask for file
# print('Okay, before we start, do you want to use the builtin file or an external one?')

# Run
main_scene(main_file)
