import requests
import random

icao24 = "406591"
api_base_url = "https://www.airport-data.com/api/"
endpoint_path = f"ac_thumb.json?m={icao24}&n=1"
endpoint = f"{api_base_url}{endpoint_path}"
r = requests.get(endpoint)
json_res = r.json()

print(json_res['data'][0]['image'])

