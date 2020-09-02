from pymongo import MongoClient
from opensky_api import OpenSkyApi
import pprint
from threading import Timer



uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.get_database("aviation")


def find(icao):
    found_planes = []
    collection = db.get_collection("planes_24aug")
    filter_ = {
        "$and": [ { 
            "icao24": icao
        }, 
        { 
            "manufacturername": { "$ne": "" } 
        } 
        ] }

    projection_ = {
        "_id": 0,
        "icao24": 1,
        "manufacturername": 1,
        "model": 1, 
        "registration": 1, 
        "operator": 1, 
        "owner": 1
    }
    cursor = collection.find(filter=filter_, projection=projection_)
    for icao_code in cursor:
        return icao_code


def get_api_resp():
    payload_keys = ['icao24', 'baro_altitude', 'velocity', 'vertical_rate', 'longitude', 'latitude', 'on_ground']
    icao24_lst = []
    try:
        api = OpenSkyApi("johnsmoth", "LennukidOnLahedad")
        states = api.get_states(time_secs=0, icao24=None, serials=None, bbox=(57,60,22,28))
        for s in states.states:
            # print(f"LINE50: STATES: {s}")
            payload_values = []
            payload_values.extend([s.icao24, s.baro_altitude, s.velocity, s.vertical_rate, s.longitude, s.latitude, s.on_ground])
            icao24data = dict(zip(payload_keys, payload_values))
            icao24_lst.append(icao24data)
    except Exception as e:
        print(e)
    return icao24_lst



api_res = [{'icao24': '511103', 'baro_altitude': 441.96, 'velocity': 44.64, 'vertical_rate': 1.3, 'longitude': 24.8574, 'latitude': 59.3288}, {'icao24': '502d2a', 'baro_altitude': 266.7, 'velocity': 34.68, 'vertical_rate': -2.28, 'longitude': 27.8515, 'latitude': 57.2946}, {'icao24': '463af3', 'baro_altitude': 6446.52, 'velocity': 179.56, 'vertical_rate': 10.08, 'longitude': 24.963, 'latitude': 58.8598}, {'icao24': '461e1b', 'baro_altitude': 11887.2, 'velocity': 235.5, 'vertical_rate': 0, 'longitude': 24.2586, 'latitude': 57.7826}, {'icao24': 'ae57ab', 'baro_altitude': 106.68, 'velocity': 8.37, 'vertical_rate': -1.3, 'longitude': 24.4442, 'latitude': 57.1076}, {'icao24': '500153', 'baro_altitude': 11277.6, 'velocity': 245.12, 'vertical_rate': 0.33, 'longitude': 22.9342, 'latitude': 57.4065}, {'icao24': '896209', 'baro_altitude': 10363.2, 'velocity': 225.39, 'vertical_rate': 0, 'longitude': 27.2213, 'latitude': 57.9496}, {'icao24': '4601fb', 'baro_altitude': 1844.04, 'velocity': 133.05, 'vertical_rate': -13.98, 'longitude': 24.5778, 'latitude': 59.5434}, {'icao24': '484f17', 'baro_altitude': 5943.6, 'velocity': 197.24, 'vertical_rate': 16.58, 'longitude': 24.3504, 'latitude': 59.9306}, {'icao24': '5113cf', 'baro_altitude': None, 'velocity': 8.23, 'vertical_rate': None, 'longitude': 24.824, 'latitude': 59.416}, {'icao24': '5113d9', 'baro_altitude': None, 'velocity': 2.83, 'vertical_rate': None, 'longitude': 24.8062, 'latitude': 59.418}, {'icao24': '3e8e96', 'baro_altitude': 5280.66, 'velocity': 148.87, 'vertical_rate': 10.73, 'longitude': 23.9731, 'latitude': 58.6957}, {'icao24': '43beb2', 'baro_altitude': 11277.6, 'velocity': 255.19, 'vertical_rate': 0, 'longitude': 26.3353, 'latitude': 57.8131}, {'icao24': '4242e9', 'baro_altitude': 11285.22, 'velocity': 240.09, 'vertical_rate': 0, 'longitude': 25.2946, 'latitude': 57.5199}, {'icao24': '461f2f', 'baro_altitude': 9723.12, 'velocity': 235.97, 'vertical_rate': -11.05, 'longitude': 22.9281, 'latitude': 59.6583}, {'icao24': '461f35', 'baro_altitude': 11887.2, 'velocity': 233.78, 'vertical_rate': -5.2, 'longitude': 23.6566, 'latitude': 59.774}, {'icao24': '424477', 'baro_altitude': 10668, 'velocity': 235.86, 'vertical_rate': 0, 'longitude': 26.0436, 'latitude': 57.9576}, {'icao24': '7808b0', 'baro_altitude': 11582.4, 'velocity': 239.04, 'vertical_rate': 0, 'longitude': 27.73, 'latitude': 59.3855}]
db_res = [{'icao24': '461e1b', 'registration': 'OH-LKL', 'manufacturername': 'Embraer', 'model': 'EMB-190 LR', 'operator': 'TEST0', 'owner': ''}, {'icao24': '896209', 'registration': 'A6-EGH', 'manufacturername': 'Boeing', 'model': '777 31HER', 'operator': '', 'owner': 'Emirates Airline'}, {'icao24': '4601fb', 'registration': 'OH-ATN', 'manufacturername': 'Avions De Transport Regional', 'model': 'ATR 72 500', 'operator': '', 'owner': 'Nordic Regional Airlines'}, {'icao24': '484f17', 'registration': 'PH-BGX', 'manufacturername': 'Boeing', 'model': '737NG 7K2/W', 'operator': '', 'owner': 'Klm Royal Dutch Airlines'}, {'icao24': '43beb2', 'registration': 'VP-BIN', 'manufacturername': 'Boeing', 'model': 'B747-8F', 'operator': 'Airbridge Cargo', 'owner': ''}, {'icao24': '4242e9', 'registration': 'VP-BQK', 'manufacturername': 'Airbus', 'model': 'Airbus A319 111', 'operator': '', 'owner': 'Rossiya Russian Airlines'}, {'icao24': '461f2f', 'registration': 'OH-LVB', 'manufacturername': 'Airbus', 'model': 'A319 112', 'operator': '', 'owner': 'Finnair'}, {'icao24': '461f35', 'registration': 'OH-LVH', 'manufacturername': 'Airbus', 'model': 'A319 112', 'operator': '', 'owner': 'Finnair'}, {'icao24': '7808b0', 'registration': 'B-6139', 'manufacturername': 'Airbus', 'model': 'A380 841', 'operator': '', 'owner': 'China Southern Airlines'}]


def merge_data(api_res, db_res):
    merged = []
    for i, _ in enumerate(api_res):
        dct = api_res[i].copy()
        for j, _ in enumerate(db_res):
            try:
                if api_res[i]['icao24'] ==  db_res[j]['icao24']:
                    dct.update(db_res[j])
                    merged.append(dct)
            except IndexError:
                continue
    return merged



def geo_coords(data):
    coords = []
    for element in data:
        if element['on_ground'] != True:
            # print(f"ELEMENT IS {element}")
            # print(f"ELEMENT IS {element['latitude']}")
            # print(f"ELEMENT IS {element['longitude']}")
                    # "coordinates": [24, 58]
            coords.append({
                "geometry": {
                    "type": "Point",
                    "coordinates": [element['longitude'], element['latitude']]
                    },
                    "type": "Feature",
                    "properties": { 
                        "id": element['icao24']
                    }
                
            })
    return coords


def get_data():
    response = []
    api_res = get_api_resp()
    print(f"{api_res=}")
    geo_coords_task = geo_coords(api_res)
    for plane in api_res:
        res = find(plane['icao24'])
        if res != None:
            response.append(res)
    merged_data_task = merge_data(api_res, response)

    # print(f"GEO DATA: {geo_coords_task}")
    # print(f"MERGED DATA: {merged_data_task}")
    return (merged_data_task), (geo_coords_task)

flights, geoJSON = get_data()

if __name__ == "__main__":
    flights, geoJSON = get_data()
    print(geoJSON)
    print(len(geoJSON))
    # get_data()


