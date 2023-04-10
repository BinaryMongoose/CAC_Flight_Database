import os
from pathlib import Path, PureWindowsPath


restarts = {}
restart_index = []

home_path = Path(__file__).resolve()

data_path = home_path.parents[1] / PureWindowsPath('data/RAW_HB/FILE_0.csv')
out_path = home_path.parents[1] / PureWindowsPath('data/out/FILE_0')
with open(data_path) as f:
    file = f.readlines()

true_header = file[0]

for index, line in enumerate(file):
    if line == true_header:
        restart_index.append(index)

for i in range(0, len(restart_index)):
    if i + 1 >= len(restart_index):
        break
    else:
        restarts[i] = file[restart_index[i]:restart_index[i + 1]]

print(' +++++ FILE INFO +++++')
print(f'The file had {len(restart_index)} restarts.')
print(f'The file is {len(file)} lines long.')

try:
    os.mkdir(out_path)
except OSError:
    print(f'Could not create folder in {out_path}. Folder already exists.')

print('\nCreated Files:')
for index, file, in restarts.items():
    file_name = f'FILE_{index}.csv'
    f_path = PureWindowsPath.joinpath(out_path, file_name)
    with open(f_path, 'w') as f:
        f.seek(0)
        f.writelines(file)
        f.truncate()

    print(f'\t - File {file_name} was created.')



