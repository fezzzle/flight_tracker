from pymongo import MongoClient
from opensky_api import OpenSkyApi
import pprint
import threading
import time


uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.get_database("aviation")


def find(icao):
    found_planes = []
    collection = db.get_collection("planes_3sept")
    filter_ = {
        "$and": [ { "icao24": icao }, { "manufacturername": { "$ne": "" } } ] }
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
            payload_values = []
            payload_values.extend([s.icao24, s.baro_altitude, s.velocity, s.vertical_rate, s.longitude, s.latitude, s.on_ground])
            icao24data = dict(zip(payload_keys, payload_values))
            icao24_lst.append(icao24data)
    except Exception as e:
        print(e)
    return icao24_lst


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
            coords.append({"geometry": {"type": "Point", "coordinates": [element['longitude'], element['latitude']]}, "type": "Feature", "properties": {"id": element['icao24'], "message": "Hello!", "iconSize": [30, 30]}})
    return coords


def get_data():
    while True:
        response = []
        api_res = get_api_resp()
        geo_coords_task = geo_coords(api_res)
        for plane in api_res:
            res = find(plane['icao24'])
            if res != None:
                response.append(res)
        merged_data_task = merge_data(api_res, response)
        for listener in listeners:
            listener.on_data(merged_data_task, geo_coords_task)
        print("Got data from GET_DATA")
        
        time.sleep(10)

listeners = []

def add_listener(listerner):
    listeners.append(listerner)

t1 = threading.Thread(target=get_data)
t1.start()
