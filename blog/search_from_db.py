from pymongo import MongoClient
from opensky_api import OpenSkyApi
import pprint
import threading
import time
# from blog import settings as ENV


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
        # api = OpenSkyApi(ENV.OPEN_SKY_API_USER, ENV.OPEN_SKY_API_PW)
        api = OpenSkyApi("johnsmoth", "ILovePlanes098")
        states = api.get_states(time_secs=0, icao24=None, serials=None, bbox=(57.5,59,21.5,28))
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
        print(element)
        if element['on_ground'] != True:
            coords.append(
                {
                    "geometry": {
                        "type": "Point", "coordinates": [element['longitude'], element['latitude']]}, 
                        "type": "Feature", "properties": {
                            "id": element['registration'], 
                            "speed": element['velocity'], 
                            "altitude": element['baro_altitude'], 
                            "manufacturer": element['manufacturername'],
                            "owner": element['owner'],
                            "model": element['model'], 
                            "iconSize": [30, 30]}})
    return coords


def airspace_save_point(data):
    collection = db.get_collection("planes_visited")
    for plane in data:
        cursor = collection.find_one({"registration": plane['registration']})
        # If plane is not in the DB, add it
        if cursor != None:
            print("Got the plane!")
            collection.update( { "registration": plane['registration'] }, { "$addToSet": {  "flights.0.flight_data": {"latitude": plane['latitude'], "longitude": plane['longitude'], "time_stamp": time.time()} } } )
            # db.planes_visited.update( { "registration": "G-VNEW" }, { $addToSet: {  "flights.0.flight_data": {"latitude": 35.333, "longitude": 38.55555} } } )

        else:
            data_to_store = {
                "registration": plane['registration'],
                "manufacturername": plane['manufacturername'],
                "model": plane['model'],
                "flights": [
                    {
                        "enter": time.time(),
                        "left": None,
                        "flight_data": [
                            {
                                "latitude": plane['latitude'],
                                "longitude": plane['longitude'],
                                "time_stamp": time.time()
                            }
                        ]
                    }
                ]
            }
            db.planes_visited.insert_one(data_to_store)
            print("No, this plane does not exist in the DB. Adding it")




def get_data():
    while True:
        planes_in_db = []
        planes_not_in_db = []
        api_res = get_api_resp()
        for plane in api_res:
            res = find(plane['icao24'])
            if res != None:
                planes_in_db.append(res)
            elif res == None and plane['on_ground']:
                pass
            else:
                planes_not_in_db.append(plane)

        merge_data_in_DB = merge_data(api_res, planes_in_db)
        airspace_save_point(merge_data_in_DB)
        get_geo_json = geo_coords(merge_data_in_DB)
        for listener in listeners:
            listener.on_data(merge_data_in_DB, get_geo_json)

        # print(f"PLANES IN DB: {merge_data_in_DB}")
        # print(f"PLANES NOT IN DB: {planes_not_in_db}")
        # print(f"TOTAL PLANES IN AIRSPACE: {len(merge_data_in_DB)} + {len(planes_not_in_db)}")
        time.sleep(10)

listeners = []

def add_listener(listerner):
    listeners.append(listerner)

t1 = threading.Thread(target=get_data)
t1.start()
