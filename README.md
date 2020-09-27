# Flight tracker
My pet project which is created in Python, javaScript and MongoDB

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## Technologies
Project is created with:
* Python 3.8
* Mapbox GL JS v1.12.0
* MongoDB
* Flask v1.1
* Bulma

## Setup
1. Download aircraftDatabase.csv from [Opensky-network](https://opensky-network.org/datasets/metadata/)
2. Run mongo: ```mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork```
3. Create ```Aviation``` DB and import ```aircraftDatabase.csv``` and create a collection named ```planes_visited``` inside aviation DB
4. Install python API from [Opensky Python API](https://github.com/openskynetwork/opensky-api)
5. Set environmental variable in shell: ```export FLASK_APP=run```
6. ```flask run```


## Images

![Map](https://github.com/fezzzle/flight_tracker/blob/master/map.png?raw=true)
![Planes](https://github.com/fezzzle/flight_tracker/blob/master/Planes.png?raw=true)