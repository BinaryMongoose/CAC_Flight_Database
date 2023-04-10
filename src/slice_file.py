import os
from pathlib import Path

home_path = Path(__file__).resolve()

data_path = home_path.parents[1] / Path('data/RAW_HB/FILE_0.csv')
out_path = home_path.parents[1] / Path('data/out/FILE_0')


def slice_file(raw_path: Path) -> dict:
    restart_index = []
    sliced_file = {}
    
    # Storing file in collection
    with open(raw_path) as raw_file:
        file = raw_file.readlines()
    true_header = file[0]
    
    # Creating a dictionary
    for index, line in enumerate(file):
        if line == true_header:
            restart_index.append(index)
    
    for i in range(0, len(restart_index)):
        if i + 1 >= len(restart_index):
            break
        else:
            sliced_file[i] = file[restart_index[i]:restart_index[i + 1]]
            
    return sliced_file


try:
    os.mkdir(out_path)
except OSError:
    print(f'Could not create folder in {out_path}. Folder already exists.')


def create_files(path: Path, sliced_file: dict, file_name: str) -> None:
    print('\nCreated Files:')
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


create_files(out_path, slice_file(data_path), 'YAY')
