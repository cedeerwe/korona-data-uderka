import requests, json
import csv
from openrouteservice import client

def req_url(city_name):
    return 'https://nominatim.openstreetmap.org/search?city={}&format=json&country=Slovakia'.format(city_name)

villages_file = 'villages.json'
geo_file = "geo.csv"

with open(villages_file) as villages_stream:
    with open(geo_file, 'w') as file:
        villages = json.load(villages_stream)
        writer = csv.writer(file)

        for village in villages:
            r = requests.get(req_url(village['fullname'])).json()
            if len(r) > 0:
                row_output = [village['fullname']]
                for found_village in r:
                    row_output += found_village['lat'], found_village['lon']

                writer.writerow(row_output)
                print("{} done".format(village['fullname']))
            else:
                writer.writerow([village['fullname'], 0, 0])
