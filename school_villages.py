import urllib.request
import pandas as pd
import urllib.parse
from bs4 import BeautifulSoup
from collections import defaultdict
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context


VILLAGE_IN_URL = 'VILLAGE_IN_URL'
REGION_IN_URL = 'REGION_IN_URL'
VILLAGE = 'village_name'
REGION = 'district_name'
WIKI_ADRESS = 'WIKI_ADRESS'
BACK_UP_WIKI_ADRESS = 'BACK_UP_WIKI_ADRESS'
POPULATION = 'population'


obce = "https://raw.githubusercontent.com/cedeerwe/korona-data-uderka/master/pairs.csv"

obce = pd.read_csv(obce, names=['village_id', 'village_name', 'district_id', 'district_name'])
obce[VILLAGE] = obce[VILLAGE].str.replace(' ','_')

def getUrl(village_name):
    return 'http://mapaskol.iedu.sk/dogrss/getSearchResult.aspx?q=all---{}---------all------all---GYM_GYM-ND_SO%C5%A0_KON_S%C5%A0-ZZ---all---all------ASC'.format(urllib.parse.quote(village_name))
    # return 'http://mapaskol.iedu.sk/dogrss/getSearchResult.aspx?q=all---{}---------all------all---M%C5%A0_Z%C5%A0-ZZ_Z%C5%A0_Z%C5%A0-ND_Z%C5%A0-ZZ_GYM_GYM-ND_SO%C5%A0_KON_S%C5%A0-ZZ---all---all------ASC'.format(urllib.parse.quote(village_name))

villages_to_schools = defaultdict(list)

for index, row in obce.iterrows():
  url = getUrl(row['village_name'])
  page = urllib.request.urlopen(url)
  soup = BeautifulSoup(page)
  trs = soup.find_all('tr')
  for tr in trs:
    tds = list(tr.find_all('td'))
    l = []
    for td in tds:
      l.append(td.string)

    if len(l) > 2: 
        villages_to_schools[row['village_name']].append({'name':l[1], 'students': l[2]})
    else: 
        print('lennn')

    print('finished {}'.format(row['village_name']))

import json
with open('middle_schools_with_students.json', 'w') as fp:
    json.dump(villages_to_schools, fp)    

