import motor.motor_asyncio
from opensky_api import OpenSkyApi
import asyncio
import time


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
        # await print_icao(icao_code)
        # found_planes.append(icao_code)
        return icao_code
    # return found_planes


async def get_api_resp():
    payload_keys = ['icao24', 'baro_altitude', 'origin_country', 'velocity', 'vertical_rate', 'squawk']
    icao24_lst = []
    try:
        api = OpenSkyApi("johnsmoth", "LennukidOnLahedad")
        states = api.get_states(time_secs=0, icao24=None, serials=None, bbox=(57,60,22,28))
        for s in states.states:
            # print(s.icao24)
            payload_values = []
            payload_values.extend([s.icao24, s.baro_altitude, s.origin_country, s.velocity, s.vertical_rate, s.squawk])
            data = dict(zip(payload_keys, payload_values))
            icao24_lst.append(data)
    except Exception as e:
        print(e)
    return icao24_lst

async def get_api_resp_fake():
    time.sleep(0.1)
    return [{'icao24': '47a721', 'baro_altitude': 2857.5, 'origin_country': 'Norway', 'velocity': 173.01, 'vertical_rate': -10.08, 'squawk': '2561'}, {'icao24': '780f3e', 'baro_altitude': 10058.4, 'origin_country': 'China', 'velocity': 268.33, 'vertical_rate': 0.33, 'squawk': '2557'}, {'icao24': '502cdc', 'baro_altitude': 457.2, 'origin_country': 'Latvia', 'velocity': 41.31, 'vertical_rate': -0.65, 'squawk': '2000'}]

async def merge_data(api_res, db_res):
    merged = []
    for i, _ in enumerate(api_res):
        dct = api_res[i].copy()
        try:
            if api_res[i]['icao24'] == db_res[i]['icao24']:
                dct.update(db_res[i])
                merged.append(dct)
        except IndexError:
            continue

    print(merged)



async def main():
    response = []
    task = asyncio.create_task(get_api_resp_fake(), name="api_call")
    await task
    # icao_lst = await get_api_resp()
    for plane in task.result():
        res = await find(plane['icao24'])
        if res != None:
            response.append(res)

    # print(f"LINE82: {response}")
    # print()
    # print(f"LINE77: {task.result()}")
    # print()
    # print(response)
    await merge_data(task.result(), response)
    return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

