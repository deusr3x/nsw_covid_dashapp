import requests
import pandas as pd
import datetime
import json

base_url = 'https://data.nsw.gov.au/data'
initial_url = '/api/3/action/datastore_search?resource_id=21304414-1ff1-4243-a5d2-f52778048b29'
today = datetime.datetime.today().strftime('%Y-%m-%d')
d = requests.get(base_url+initial_url)
p = d.json()

p['result']['offset'] = 0
res = []
res.append(p)
while p['result']['total'] > p['result']['offset']:
    new_url = base_url+p['result']['_links']['next']
    d = requests.get(new_url)
    p = d.json()
    res.append(p)
g = []
for i in range(len(res)):
    g += res[i]['result']['records']

today = datetime.datetime.today().strftime('%Y-%m-%d')
df = pd.DataFrame(g)
if '_id' not in df.columns:
    df = df.reset_index()
    df = df.rename(columns={'index': '_id'})
df.to_csv(f'output_data-{today}.csv', index=False)

with open('lgamap_rs.json', 'r') as f:
    lgas = json.load(f)

a = []
for i in lgas['features']:
    a.append([i['id'],i['properties']['nsw_lga__3'],i['properties']['nsw_lga__2']])

df = pd.read_csv(f'output_data-{today}.csv')
df['lganame_cap'] = df['lga_name19'].str.upper().str.split('(', expand=True)[0].str.strip()

dd = pd.DataFrame(a, columns=['id', 'name', 'name2'])

df2 = df.merge(dd,how='left',left_on='lganame_cap', right_on='name')
s = df2.groupby(['id','lga_name19'])['_id'].count()
df3 = s.to_frame()

df3.reset_index(inplace=True)
df3 = df3.rename(columns={'_id': 'infections', 'lga_name19': 'LGAName'})
df3.to_csv('mapdata.csv', index=False)
