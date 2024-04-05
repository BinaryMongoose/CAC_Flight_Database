from itertools import zip_longest
import pandas as pd
from pathlib import Path
from typing import Dict, List

from Meta import Meta


class Payload(Meta):
    data = None

    def __init__(self, path: Path):
        try:
            self.data = pd.read_csv(path)
        except FileNotFoundError:
            raise FileNotFoundError
        super().__init__(self.meta, path)

    def create_base(self, header_format: Dict, other: List) -> None:
        header = list(self.data.columns)
        for name in header:
            self.meta[name] = {}
            parts = name.split(header_format['delimiter'])
            for item, value in zip_longest(header_format['items'] + other, parts, fillvalue=None):
                self.meta[name][item] = value
