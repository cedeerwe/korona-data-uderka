# zo stranky http://www.sodbtn.sk/obce/obce_zaklad_mapa.php
# network tab, komunikacia obce_www.topojson

import json

with open('raw_mapa_obci.json', encoding='utf-8-sig') as f:
    d = json.load(f)

parsed_data = [{
    'obec': data['properties']['OBEC'],
    'okres': data['properties']['OKRES'],
    'id_okres': data['properties']['ID_OKRES'],
    'kraj': data['properties']['KRAJ'],
    'typ': data['properties']['typ'],
    'pocet_obyvatelov_2013': data['properties']['po_2013']
} for data in d['objects']['collection']['geometries']]

with open("obce_obyvatelia.json", "w") as file:
    json.dump(parsed_data, file)
