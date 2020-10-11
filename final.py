obce_obyvatelia = 'obyvatelia/obce_obyvatelia_fixed.json'
pocty_pozitivnych = 'pocet_pozitivnych_obce_24_09_2020-07_10_2020.csv'
schools = 'middle_schools_with_students_fixed.json'

import json
import csv
import pandas
from concat import get_pairing


with open(obce_obyvatelia, 'r') as f:
    with open(schools, 'r') as school_stream:
        schools_db = json.load(school_stream)
        main = json.load(f)
        pos = pandas.read_csv(pocty_pozitivnych)

        obec_to_pos = {}
        for index, row in pos.iterrows():
            obec_to_pos[row['Obec']] = row['SUM of Pocet']

        df = pandas.DataFrame(main)
        def apply_covid(row):
            return obec_to_pos[row['obec']] if row['obec'] in obec_to_pos else 0

        def apply_schools_count(row):
            return len(schools_db[row['obec']]) if row['obec'] in schools_db else 0

        def apply_max_school(row):
            _max = 0
            _max_school = ""
            if row['obec'] not in schools_db:
                return {}

            for school in schools_db[row['obec']]:
                if school['students'] != "N*" and int(school['students']) > _max:
                    _max = int(school['students'])
                    _max_school = school
            
            return _max_school

        def get_school_name(school): return school['name'] if 'name' in school else None
        def get_school_students(school): return school['students'] if 'students' in school else None

        df['covid_positive'] = df.apply(apply_covid, axis=1)
        df['schools'] = df.apply(apply_schools_count, axis=1)
        df['max_school_students'] = df.apply(lambda row: get_school_students(apply_max_school(row)), axis=1)
        df['max_school_name'] = df.apply(lambda row: get_school_name(apply_max_school(row)), axis=1)
        
        df.to_csv('final.csv')
