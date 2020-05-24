import json

with open('lgamap.json', 'r') as f:
    lgas = json.load(f)

newlgas = lgas
for i, v in enumerate(lgas['features']):
    a = v['geometry']['coordinates'][0][0]
    b = a[::5]
    b[-1] = a [-1]
    # a[0][0] = b
    newlgas['features'][i]['geometry']['coordinates'][0][0] = b

with open('lgamap_rs.json', 'w') as f:
    json.dump(newlgas, f)
