# Little NSW COVID Dashboard

This project will also assume that python 3 and pip are already installed.


## Mapbox token
First you will need to go to www.mapbox.com and create a free account to get a public Mapbox Access Token.  Once you have the token set the environment variable as:

`export MAPBOXTOKEN=...`

## Setting Everything Else Up
To get started run:

`make install`

This will:
1. Download a geojson file for NSW LGAs from [here](https://data.gov.au/geoserver/nsw-local-government-areas/wfs?request=GetFeature&typeName=ckan_f6a00643_1842_48cd_9c2f_df23a3a1dc1e&outputFormat=json)
2. Create a virtual environment using `venv`
3. Install required packages via `pip` (see `requirements.txt`)
4. Process the LGA geojson file by trimming down the number of points

## Running the App
Once this is done do:

`make run`

This will get the latest data from the NSW data.nsw.gov.au site [here](https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id=21304414-1ff1-4243-a5d2-f52778048b29)

Then it will launch the app, you will be able to navigate to `127.0.0.1:8050` to see the dashboard.

## Cleaning Up
`make clean` will remove all files and the virtual environment.