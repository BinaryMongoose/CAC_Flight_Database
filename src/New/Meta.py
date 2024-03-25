from pathlib import Path

import json
import pandas as pd

home_path = Path(__file__).resolve()

data_path = home_path.parents[2] / Path('data/Payload/CAC_Spring_2023/Payload_2.csv')

class MetaData:
    """
    Every sensor has a list of measurements. Each of these are stored in a dictionary, sensor_items.

    Example:
        {bme680 : [temp, humid, pressure], ltr30 : [uv]}
    """

    name = ""
    sensor_items = {}
    notes = []

    def __init__(self, file):
        self.file_path = Path(file)
        self.name = self.file_path.stem
        self.data = pd.read_csv(home_path.parents[1] / self.file_path)
        self.generate_data()

    def generate_data(self):
        header = list(self.data.columns)

        # Getting each sensor used.
        for name in header:
            # Finds the underscore in the name.
            sep_index = name.find('_')
            if sep_index == -1:
                print(f'{name} does not have any items.')
                continue
            # Everything to the right of the underscore is the name of the sensor
            sensor = name[:sep_index]
            # Create a sensor entry in the sensor_items dictionary.
            self.sensor_items[sensor] = []

        # Getting what each sensor measures.
        for name in header:
            # Find the underscore.
            sep_index = name.find('_')
            if sep_index == -1:
                print(f'{name} does not have any items.')
                continue
            # Everything to the RIGHT of the underscore is a sensor.
            sensor = name[:sep_index]
            # Everything to the LEFT of the underscore is a item.
            item = name[sep_index + 1:]
            # Using the sensor as a key, add all items found to the sensor.
            self.sensor_items[sensor].append(item)

    def store_meta(self):
        meta_path = home_path.parents[0] / self.file_path.parents[0] / f'{self.name}.meta'
        with open(meta_path, 'w') as out:
            sensor_items = json.dumps(self.sensor_items, sort_keys=True, indent=4)
            out.writelines(sensor_items)




if __name__ == '__main__':
    Meta = MetaData(data_path)

