const currentFlights = 'http://127.0.0.1:5000/aviation/api';
const flightData = 'http://127.0.0.1:5000/aviation/flight_data';
let markers = [];
let popups = [];


mapboxgl.accessToken = 'pk.eyJ1Ijoiam9obnNtb3RoIiwiYSI6ImNrZWEycnRrdjAyZzYyd3AwYml5MjBuaXAifQ.CJqLW89MSuqwH-ijHwx_0w';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [25, 58.6],
    zoom: 7
});

function main() {
    removeIcons()
    callCurrentFlights()
    callFlightDataFromDB()
}

function callFlightDataFromDB() {
    var request = new XMLHttpRequest();
    request.open('GET', flightData, true);
    request.onload = function() {
        let flights = []
        if (this.status >= 200 && this.status < 400) {
            let json = get_geojson(this.response)
            let planeFlights = json.flights[0].flight_data
            planeFlights.forEach((flight) => {
                console.log("LINE 30: ", json.flights[0])
                flights.push(Array.from([flight.longitude, flight.latitude]))
            });
            try {
                map.addSource(flight.registration, {
                    'type': 'geojson',
                    'data': {
                        'type': 'Feature',
                        'properties': {},
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': flights
                        }
                    }
                });
                map.addLayer({
                    'id': 'route',
                    'type': 'line',
                    'source': 'route',
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    'paint': {
                        'line-color': '#89c',
                        'line-width': 2
                    }
                });
            } catch (e) {
                console.log(e)
            }
        };
    };
    request.send();
}

function callCurrentFlights() {
    var request = new XMLHttpRequest();
    request.open('GET', currentFlights, true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            let json = get_geojson(this.response)
            json.forEach(element => {
                setMarkerData(element)
            });
        }
    };
    request.send();
}

function get_geojson(resp) {
    return JSON.parse(resp);
};

function setMarkerData(data) {
    let html = `
    REG: ${data.properties.id},
    SPD: ${data.properties.speed},
    OWN: ${data.properties.owner},
    PLANE: ${data.properties.model},
    ALT: ${data.properties.altitude}
    `
    // create a DOM element for the marker
    var el = document.createElement('div');
    el.className = 'marker';
    el.style.backgroundImage = 'url(http://127.0.0.1:5000/static/marker.png)';
    el.style.width = data.properties.iconSize[0] + 'px';
    el.style.height = data.properties.iconSize[1] + 'px';

    var marker = new mapboxgl.Marker(el)
    .setLngLat(data.geometry.coordinates)
    .setRotation(90)
    .addTo(map);
    markers.push(marker)

    var popup = new mapboxgl.Popup({maxWidth: '300px', closeOnClick: false})
    .setLngLat(data.geometry.coordinates)
    .setHTML(html)
    .addTo(map);
    popups.push(popup)
};

function setIntervalAndExecute(fn, t) {
    map.on('load', function() {
        fn();
        return(setInterval(fn, t));
    });
}

function removeIcons() {
    markers.forEach((marker) => marker.remove());
    markers = [];
    popups.forEach((popup) => popup.remove());
    popups = [];
  }

setIntervalAndExecute(main, 5000);









