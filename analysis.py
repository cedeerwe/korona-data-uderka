import pandas as pd

df = pd.read_csv("pop.csv")

print(df[df['population'] > 500])