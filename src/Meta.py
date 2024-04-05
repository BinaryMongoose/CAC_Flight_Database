from pathlib import Path
import json
from typing import Dict


class Meta:
    meta = {}
    meta_path = Path()

    def __init__(self, items: Dict, path: Path) -> None:
        """
        Creates an object that stores the information associated with a row in a CSV file.

        :param items:
        :param path:
        """
        self.file_path = path
        self.meta_path = self.file_path.parents[0] / f'{self.file_path.stem}.meta'

        # Initializing the meta with items.
        for name, item in items.items():
            self.meta[name] = item

    def store(self) -> None:
        """
        the metadata is stored with the original CSV file.
        The meta file has the same name as the CSV file, but with the extension .meta
        :return:
        """

        with open(self.meta_path, 'w') as out:
            dump = json.dumps(self.meta, indent=4)
            out.writelines(dump)

    def load(self):
        with open(self.meta_path, 'r') as file:
            self.meta = json.load(file)
