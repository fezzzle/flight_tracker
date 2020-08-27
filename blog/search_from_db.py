import motor.motor_asyncio
from opensky_api import OpenSkyApi
import asyncio
import pprint


uri = "mongodb://localhost:27017/"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.get_database("aviation")

# async def print_icao(icao_code):
#     print(icao_code)


async def find(icao):
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
    async for icao_code in cursor:
        return icao_code


async def get_api_resp():
    payload_keys = ['icao24', 'baro_altitude', 'velocity', 'vertical_rate', 'longitude', 'latitude']
    icao24_lst = []
    # geocoords_keys = ['lng', 'lat']
    # geocoords = []
    try:
        api = OpenSkyApi("johnsmoth", "LennukidOnLahedad")
        states = api.get_states(time_secs=0, icao24=None, serials=None, bbox=(57,60,22,28))
        for s in states.states:
            print(f"LINE50: STATES: {s}")
            payload_values = []
            payload_values.extend([s.icao24, s.baro_altitude, s.velocity, s.vertical_rate, s.longitude, s.latitude])
            icao24data = dict(zip(payload_keys, payload_values))
            icao24_lst.append(icao24data)

            # geo_values = []
            # geo_values.extend([s.longitude, s.latitude])
            # geodata = dict(zip(geocoords_keys, geo_values))
            # geocoords.append(geodata)
    except Exception as e:
        print(e)
    return icao24_lst


# Some testing code

# async def get_api_resp_fake():
#     time.sleep(0.1)
#     return [{'icao24': '47a721', 'baro_altitude': 2857.5, 'origin_country': 'Norway', 'velocity': 173.01, 'vertical_rate': -10.08, 'squawk': '2561'}, {'icao24': '780f3e', 'baro_altitude': 10058.4, 'origin_country': 'China', 'velocity': 268.33, 'vertical_rate': 0.33, 'squawk': '2557'}, {'icao24': '502cdc', 'baro_altitude': 457.2, 'origin_country': 'Latvia', 'velocity': 41.31, 'vertical_rate': -0.65, 'squawk': '2000'}]

api_res = [{'icao24': '511103', 'baro_altitude': 441.96, 'velocity': 44.64, 'vertical_rate': 1.3, 'longitude': 24.8574, 'latitude': 59.3288}, {'icao24': '502d2a', 'baro_altitude': 266.7, 'velocity': 34.68, 'vertical_rate': -2.28, 'longitude': 27.8515, 'latitude': 57.2946}, {'icao24': '463af3', 'baro_altitude': 6446.52, 'velocity': 179.56, 'vertical_rate': 10.08, 'longitude': 24.963, 'latitude': 58.8598}, {'icao24': '461e1b', 'baro_altitude': 11887.2, 'velocity': 235.5, 'vertical_rate': 0, 'longitude': 24.2586, 'latitude': 57.7826}, {'icao24': 'ae57ab', 'baro_altitude': 106.68, 'velocity': 8.37, 'vertical_rate': -1.3, 'longitude': 24.4442, 'latitude': 57.1076}, {'icao24': '500153', 'baro_altitude': 11277.6, 'velocity': 245.12, 'vertical_rate': 0.33, 'longitude': 22.9342, 'latitude': 57.4065}, {'icao24': '896209', 'baro_altitude': 10363.2, 'velocity': 225.39, 'vertical_rate': 0, 'longitude': 27.2213, 'latitude': 57.9496}, {'icao24': '4601fb', 'baro_altitude': 1844.04, 'velocity': 133.05, 'vertical_rate': -13.98, 'longitude': 24.5778, 'latitude': 59.5434}, {'icao24': '484f17', 'baro_altitude': 5943.6, 'velocity': 197.24, 'vertical_rate': 16.58, 'longitude': 24.3504, 'latitude': 59.9306}, {'icao24': '5113cf', 'baro_altitude': None, 'velocity': 8.23, 'vertical_rate': None, 'longitude': 24.824, 'latitude': 59.416}, {'icao24': '5113d9', 'baro_altitude': None, 'velocity': 2.83, 'vertical_rate': None, 'longitude': 24.8062, 'latitude': 59.418}, {'icao24': '3e8e96', 'baro_altitude': 5280.66, 'velocity': 148.87, 'vertical_rate': 10.73, 'longitude': 23.9731, 'latitude': 58.6957}, {'icao24': '43beb2', 'baro_altitude': 11277.6, 'velocity': 255.19, 'vertical_rate': 0, 'longitude': 26.3353, 'latitude': 57.8131}, {'icao24': '4242e9', 'baro_altitude': 11285.22, 'velocity': 240.09, 'vertical_rate': 0, 'longitude': 25.2946, 'latitude': 57.5199}, {'icao24': '461f2f', 'baro_altitude': 9723.12, 'velocity': 235.97, 'vertical_rate': -11.05, 'longitude': 22.9281, 'latitude': 59.6583}, {'icao24': '461f35', 'baro_altitude': 11887.2, 'velocity': 233.78, 'vertical_rate': -5.2, 'longitude': 23.6566, 'latitude': 59.774}, {'icao24': '424477', 'baro_altitude': 10668, 'velocity': 235.86, 'vertical_rate': 0, 'longitude': 26.0436, 'latitude': 57.9576}, {'icao24': '7808b0', 'baro_altitude': 11582.4, 'velocity': 239.04, 'vertical_rate': 0, 'longitude': 27.73, 'latitude': 59.3855}]
db_res = [{'icao24': '461e1b', 'registration': 'OH-LKL', 'manufacturername': 'Embraer', 'model': 'EMB-190 LR', 'operator': 'TEST0', 'owner': ''}, {'icao24': '896209', 'registration': 'A6-EGH', 'manufacturername': 'Boeing', 'model': '777 31HER', 'operator': '', 'owner': 'Emirates Airline'}, {'icao24': '4601fb', 'registration': 'OH-ATN', 'manufacturername': 'Avions De Transport Regional', 'model': 'ATR 72 500', 'operator': '', 'owner': 'Nordic Regional Airlines'}, {'icao24': '484f17', 'registration': 'PH-BGX', 'manufacturername': 'Boeing', 'model': '737NG 7K2/W', 'operator': '', 'owner': 'Klm Royal Dutch Airlines'}, {'icao24': '43beb2', 'registration': 'VP-BIN', 'manufacturername': 'Boeing', 'model': 'B747-8F', 'operator': 'Airbridge Cargo', 'owner': ''}, {'icao24': '4242e9', 'registration': 'VP-BQK', 'manufacturername': 'Airbus', 'model': 'Airbus A319 111', 'operator': '', 'owner': 'Rossiya Russian Airlines'}, {'icao24': '461f2f', 'registration': 'OH-LVB', 'manufacturername': 'Airbus', 'model': 'A319 112', 'operator': '', 'owner': 'Finnair'}, {'icao24': '461f35', 'registration': 'OH-LVH', 'manufacturername': 'Airbus', 'model': 'A319 112', 'operator': '', 'owner': 'Finnair'}, {'icao24': '7808b0', 'registration': 'B-6139', 'manufacturername': 'Airbus', 'model': 'A380 841', 'operator': '', 'owner': 'China Southern Airlines'}]


async def merge_data(api_res, db_res):
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


# // {"geometry": {"type": "Point", "coordinates": [-89.39509694073094, 14.482296190921412]}, "type": "Feature", "properties": {}}
async def geo_coords(data):
    coords = []
    for element in data:
        if element['on_ground'] != True:
        coords.append({
            "geometry": {
                "type": "Point",
                "coordinates": [element['longitude'], element['latitude']]},
                "type": "Feature",
                "properties": {}
            })
    return coords


async def main():
    response = []
    task = asyncio.create_task(get_api_resp(), name="api_call")
    await task
    # print(f"TASK RESULT: {task.result()}")
    geo_coords_data = await geo_coords(task.result())
    print(f"GEO DATA: {geo_coords_data}")
    for plane in task.result():
        res = await find(plane['icao24'])
        if res != None:
            response.append(res)
    merged_data = await merge_data(task.result(), response)
    # merged_data = await merge_data(api_res, db_res)
    # print(f"TASK RESULT: {task.result()}")
    # print(f"RESPONSE: {response}")

    # print(merged_data)
    # print(len(merged_data))
    return merged_data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


