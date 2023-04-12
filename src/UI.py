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
        match v:
            case 'main' | 'm':
                stripped.remove(v)
                main_scene(main_file)
            case 'h' | 'help':
                stripped.remove(v)
                text_help()
    print(stripped)
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

    data_input = get_input('Visualize - What data do you want to see?')
    for choice in data_input.copy():
        match choice:
            case 'alt':
                alt_choices = get_input('What altitude data do you want?')
                print('alt')
                data_input.remove(choice)
            case 'gps':
                gps_choices = get_input('What GPS data do you want?')
                print('gps')
                data_input.remove(choice)
            case 'acc':
                acc_choices = get_input('What acceleration data do you want?')
                print('acc')
                data_input.remove(choice)

    # Creating a list of items to present.
    for item in data_input:
        item = item.replace(" ", "_")
        item = item.replace('altitude', 'alt')
        if item in header:
            items_to_show.append(item)
        else:
            print(f'{item} does not exist.')

    time_input = get_input('''Visualize - What time frame do you want?
                           You can choose from 10:31 to 4:41.''')



    graph = main_file[items_to_show]

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
