import motor.motor_asyncio
from opensky_api import OpenSkyApi
import asyncio
import pprint


uri = "mongodb://localhost:27017/"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.get_database("aviation")

async def print_icao(icao_code):
    print(icao_code)


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
    try:
        api = OpenSkyApi("johnsmoth", "LennukidOnLahedad")
        states = api.get_states(time_secs=0, icao24=None, serials=None, bbox=(57,60,22,28))
        for s in states.states:
            payload_values = []
            payload_values.extend([s.icao24, s.baro_altitude, s.velocity, s.vertical_rate, s.longitude, s.latitude])
            data = dict(zip(payload_keys, payload_values))
            icao24_lst.append(data)
    except Exception as e:
        print(e)
    return icao24_lst


# Some testing code

# async def get_api_resp_fake():
#     time.sleep(0.1)
#     return [{'icao24': '47a721', 'baro_altitude': 2857.5, 'origin_country': 'Norway', 'velocity': 173.01, 'vertical_rate': -10.08, 'squawk': '2561'}, {'icao24': '780f3e', 'baro_altitude': 10058.4, 'origin_country': 'China', 'velocity': 268.33, 'vertical_rate': 0.33, 'squawk': '2557'}, {'icao24': '502cdc', 'baro_altitude': 457.2, 'origin_country': 'Latvia', 'velocity': 41.31, 'vertical_rate': -0.65, 'squawk': '2000'}]

# api_res = [{'icao24': '502cf2', 'baro_altitude': 975.36, 'origin_country': 'Latvia', 'velocity': 50.08, 'vertical_rate': 0.33, 'squawk': '0073'}, {'icao24': '4007f6', 'baro_altitude': 11277.6, 'origin_country': 'United Kingdom', 'velocity': 273.13, 'vertical_rate': 0, 'squawk': '4613'}, {'icao24': '4840cf', 'baro_altitude': 11582.4, 'origin_country': 'Kingdom of the Netherlands', 'velocity': 237.97, 'vertical_rate': -0.33, 'squawk': '1311'}, {'icao24': '4245a7', 'baro_altitude': 11582.4, 'origin_country': 'United Kingdom', 'velocity': 211.48, 'vertical_rate': -0.33, 'squawk': '1166'}, {'icao24': '461f38', 'baro_altitude': 8877.3, 'origin_country': 'Finland', 'velocity': 221.22, 'vertical_rate': -10.73, 'squawk': '4541'}, {'icao24': '424407', 'baro_altitude': 10668, 'origin_country': 'United Kingdom', 'velocity': 262.55, 'vertical_rate': 0, 'squawk': '1220'}]
# db_res = [{'icao24': '4007f6', 'registration': 'G-YMMK', 'manufacturername': 'Boeing Company', 'model': 'BOEING 777-236', 'operator': 'British Airways', 'owner': 'British Airways'}, {'icao24': '4840cf', 'registration': 'PH-BFT', 'manufacturername': 'Boeing', 'model': '747 406 SCD', 'operator': '', 'owner': 'Klm Royal Dutch Airlines'}, {'icao24': '4245a7', 'registration': 'VQ-BTY', 'manufacturername': 'Airbus', 'model': 'A319 112', 'operator': '', 'owner': 'Ural Airlines'}, {'icao24': '461f38', 'registration': 'OH-LVK', 'manufacturername': 'Airbus', 'model': 'A319 112', 'operator': '', 'owner': 'Finnair'}, {'icao24': '424407', 'registration': 'VQ-BBH', 'manufacturername': 'Boeing', 'model': '747 83QF', 'operator': '', 'owner': 'Silk Way West Airlines'}]

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


async def main():
    response = []
    task = asyncio.create_task(get_api_resp(), name="api_call")
    await task
    for plane in task.result():
        res = await find(plane['icao24'])
        if res != None:
            response.append(res)
    merged_data = await merge_data(task.result(), response)
    # merged_data = await merge_data(api_res, db_res)
    print(merged_data)
    print(len(merged_data))
    return merged_data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


