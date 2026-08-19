import pandas as pd

path = "./src/artists.csv"

df = pd.read_csv(path)

print(df.shape)