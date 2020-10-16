obce_obyvatelia = 'pop.csv'
pocty_pozitivnych = 'pocet_pozitivnych_obce_24_09_2020-07_10_2020.csv'
schools = 'middle_schools_with_students_fixed.json'
vytazenost = '_vytaz.csv'

import json
import csv
import pandas
from concat import get_pairing


with open(schools, 'r') as school_stream:
    schools_db = json.load(school_stream)
    df = pandas.read_csv(obce_obyvatelia)
    pos = pandas.read_csv(pocty_pozitivnych)
    vytaz = pandas.read_csv(vytazenost)

    obec_to_pos = {}
    for index, row in pos.iterrows():
        obec_to_pos[row['Obec']] = row['SUM of Pocet']

    # df = pandas.DataFrame(main)
    def apply_covid(row):
        return obec_to_pos[row['village_name']] if row['village_name'] in obec_to_pos else 0

    def apply_schools_count(row):
        return len(schools_db[row['village_name']]) if row['village_name'] in schools_db else 0

    def apply_max_school(row):
        _max = 0
        _max_school = ""
        if row['village_name'] not in schools_db:
            return {}

        for school in schools_db[row['village_name']]:
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

    df['positive_ratio'] = df.apply(lambda row: row['covid_positive']/row['population'], axis=1)
    df = df.sort_values(['positive_ratio'], ascending=[0])

    dist_to_vytazenost = {}
    for index, row in vytaz.iterrows():
        dist_to_vytazenost[row['area']] = float(str(row['p']).replace(',', "."))

    def a(row):
        return row['positive_ratio'] * 1

    def_vytazenost = 0.001

    def b(row):
        # vytazenost okresu
        return dist_to_vytazenost[row['district_name']] if row['district_name'] in dist_to_vytazenost else def_vytazenost

    def c(row):
        def weight_c(pop):
            C = 10000
            if pop < 500:
                return 0
            elif pop > C:
                return 1
            else:
                return pop / C

        return weight_c(float(row['population']))

    df['pos_ratio_c'] = df.apply(a, axis=1)
    df['vytazenost_okresu_c'] = df.apply(b, axis=1)
    df['vytazenost_okresu_c'] = df['vytazenost_okresu_c'].fillna(def_vytazenost)
    df['population_weight_c'] = df.apply(c, axis=1)

    df['vytazenost_okresu_c__'] = df.apply(lambda row: row['vytazenost_okresu_c'] / df['vytazenost_okresu_c'].max(), axis=1)
    df['population_weight_c__'] = df.apply(lambda row: row['population_weight_c'] / df['population_weight_c'].max(), axis=1)
    df['pos_ratio_c__'] = df.apply(lambda row: row['pos_ratio_c'] / df['pos_ratio_c'].max(), axis=1)
    print(df['vytazenost_okresu_c'].max())

    df['final_coeff'] = df['vytazenost_okresu_c__'] + df['population_weight_c__'] + df['pos_ratio_c__']
    df = df.sort_values(['final_coeff'], ascending=[0])
    # df['population_weight_c__'] = df.apply(c, axis=1)
    
    # print(df)

    from collections import defaultdict
    okres = defaultdict(int)
    s = 0
    for index, row in df.iterrows():
        okres[row['district_name']] += row['covid_positive']
        s+=row['covid_positive']

    l = []
    for key, val in okres.items():
        l.append([key, val])    

    okresy_df = pandas.DataFrame(l, columns=['area', 'positive'])

    print(df.head(20))
    # print(okresy_df)
    # print(dist_to_vytazenost)
    df.to_csv('final_dist.csv')