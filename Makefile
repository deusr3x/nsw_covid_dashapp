install: download_lga venv install_reqs process_lga

run: get_data start_app

venv:
	python -m venv env

install_reqs:
	(. "env/bin/activate" && pip install -r requirements.txt)

download_lga:
	wget -O lgamap.json "https://data.gov.au/geoserver/nsw-local-government-areas/wfs?request=GetFeature&typeName=ckan_f6a00643_1842_48cd_9c2f_df23a3a1dc1e&outputFormat=json"

process_lga:
	(. "env/bin/activate" && python trim_lgas.py)

get_data:
	(. "env/bin/activate" && python get_data.py)

start_app:
	(. "env/bin/activate" && python app.py)

clean:
	rm *.json && \
	rm -r env && \
	rm *.csv