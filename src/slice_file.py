import os
from pathlib import Path
import pprint

home_path = Path(__file__).resolve()

data_path = home_path.parents[1] / Path('data/RAW_HB/FILE_3.csv')
out_path = home_path.parents[1] / Path('data/out/FILE_3')


def setup() -> bool:
    global data_path
    home_path = Path(__file__).resolve()

    data_path = home_path.parents[1] / Path('data/RAW_HB/FILE_0.csv')
    out_path = home_path.parents[1] / Path('data/out/FILE_0')

    try:
        os.mkdir(out_path)
        return True
    except OSError:
        # print(f'Could not create folder in {out_path}. Folder already exists.')
        return False


def slice_file(raw_path: Path) -> dict:
    restart_index = []
    sliced_file = {}

    # Storing file in collection
    with open(raw_path) as raw_file:
        file = raw_file.readlines()
    true_header = file[0]

    # Creating a dictionary

    for index, line in enumerate(file):  # Makes an array of the indexes of headers.
        if line == true_header:
            restart_index.append(index)
    restart_index.append(len(file))  # Make sure to include the last line of the file.
    pprint.pprint(restart_index)

    for i in range(0, len(restart_index)):
        if i + 1 >= len(restart_index):
            break
        else:
            sliced_file[i] = file[restart_index[i]:restart_index[i + 1]]

    return sliced_file


def create_files(path: Path, sliced_file: dict, file_name: str) -> None:
    path = Path(path)

    if not path.exists():
        os.mkdir(path)

    for slice_index, file_slice, in sliced_file.items():
        slice_name = f'{file_name}_{slice_index}.csv'
        slice_path = Path.joinpath(path, slice_name)

        if slice_path.is_file():
            print(f'\t - File {slice_name} already exists.')
            continue
        else:
            try:
                with open(slice_path, 'w') as f_slice:
                    f_slice.seek(0)
                    f_slice.writelines(file_slice)
                    f_slice.truncate()
            except PermissionError:
                print(' <ERROR> Path supplied is a folder.')
                break


sliced = slice_file(data_path)
create_files(out_path, sliced, 'YAY')
