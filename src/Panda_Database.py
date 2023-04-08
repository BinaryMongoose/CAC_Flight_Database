import pandas as pd

# Read the file
data = pd.read_csv("../data/RAW_HB/FILE_0.csv", low_memory=False)

# Output the number of rows
print(f"Total rows: {len(data)}")


