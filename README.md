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
3. Create ```Aviation``` DB and import ```aircraftDatabase.csv```
4. Set environmental variable in shell: ```export FLASK_APP=run```
5. ```flask run```


## Images

![Map](https://github.com/fezzzle/flight_tracker/blob/master/map.png?raw=true)
![Planes](https://github.com/fezzzle/flight_tracker/blob/master/Planes.png?raw=true)