import motor.motor_asyncio
from opensky_api import OpenSkyApi
import asyncio


uri = "mongodb://localhost:27017/"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
db = client.get_database("aviation")

async def print_icao(icao_code):
    print(icao_code)


async def find(icao):
    collection = db.get_collection("planes_24aug")

    # filter_ = {
    #     "icao24": icao
    # }
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
        'manufacturername': 1,
        "model": 1, 
        "registration": 1, 
        "operator": 1, 
        "owner": 1,
        "categoryDescription": 1
    }
    cursor = collection.find(filter=filter_, projection=projection_)

    async for icao_code in cursor:
        await print_icao(icao_code)
    return


async def get_api_resp():
    payload_keys = ['icao24', 'baro_altitude', 'origin_country', 'velocity', 'vertical_rate', 'squawk']
    icao24_lst = []
    try:
        api = OpenSkyApi("johnsmoth", "LennukidOnLahedad")
        states = api.get_states(time_secs=0, icao24=None, serials=None, bbox=(57,60,22,28))
        for s in states.states:
            payload_values = []
            payload_values.extend([s.icao24, s.baro_altitude, s.origin_country, s.velocity, s.vertical_rate, s.squawk])
            data = dict(zip(payload_keys, payload_values))
            icao24_lst.append(data)
    except Exception as e:
        print(e)
    return icao24_lst

async def main():
    icao_lst = await get_api_resp()
    for plane in icao_lst:
        res = await find(plane['icao24'])
        print(res)
    return


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    to_list = loop.run_until_complete(main())
    print(to_list)

