import pandas as pd

df = pd.read_csv("pop_fixed.csv")

pop_key = 'pocet_obyvatelov_2013'
city_cap = 3000
total_residents = df[pop_key].sum()

living_in_big_cities = df[df[pop_key] > city_cap][pop_key].sum()

ratio = living_in_big_cities / total_residents

print(total_residents)
print("{}% lives in cities where pop(city) > {}".format(ratio * 100, city_cap))

