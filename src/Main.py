from pathlib import Path
from Payload import Payload


def main(path):
    payload = Payload(path)

    if not Path(path.parent / f'{path.stem}.meta').is_file():
        header_format = {}
        while True:
            # TODO: Add error checking
            header_format['delimiter'] = input('Delimiter: ').strip()
            header_format['items'] = input('Format: ').split(header_format['delimiter'])
            other = input("Other (for each sensor): ").split()
            break

        payload.create_base(header_format, other)
    else:
        payload.load()

    payload.store()
    print(payload.meta)


if __name__ == '__main__':
    # Everything in here is for testing.
    home_path = Path(__file__).resolve()
    data_path = home_path.parents[1] / Path('data/Payload/CAC_Spring_2023/Payload_2.csv')
    main(data_path)
