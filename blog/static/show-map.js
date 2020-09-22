const currentFlights = 'http://127.0.0.1:5000/aviation/api';
// const flightData = 'http://127.0.0.1:5000/aviation/flight_data';
let markers = [];
let popups = [];
let plane_direction_data = {}


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
    // callFlightDataFromDB()
}

function getBearing(p1, p2) {
    var lon1 = toRad(p1[0]);
    var lon2 = toRad(p2[0]);
    var lat1 = toRad(p1[1]);
    var lat2 = toRad(p2[1]);
    var a = Math.sin(lon2 - lon1) * Math.cos(lat2);
    var b = Math.cos(lat1) * Math.sin(lat2) -
        Math.sin(lat1) * Math.cos(lat2) * Math.cos(lon2 - lon1);

    var bearing = toDeg(Math.atan2(a, b));

    return bearing;
};

function toRad(degree) {
    return degree * Math.PI / 180;
}

function toDeg(radian) {
    return radian * 180 / Math.PI;
}

// function callFlightDataFromDB() {
//     var request = new XMLHttpRequest();
//     request.open('GET', flightData, true);
//     request.onload = function() {
//         let flights = []
//         if (this.status >= 200 && this.status < 400) {
//             let json = get_geojson(this.response)
//             let planeFlights = json.flights[0].flight_data
//             planeFlights.forEach((flight) => {
//                 console.log("FLIGHT: ", flight)
//                 console.log("LINE 30: ", json.flights[0])
//                 flights.push(Array.from([flight.longitude, flight.latitude]))
//             });
//             try {
//                 map.addSource(flight.registration, {
//                     'type': 'geojson',
//                     'data': {
//                         'type': 'Feature',
//                         'properties': {},
//                         'geometry': {
//                             'type': 'LineString',
//                             'coordinates': flights
//                         }
//                     }
//                 });
//                 map.addLayer({
//                     'id': 'route',
//                     'type': 'line',
//                     'source': 'route',
//                     'layout': {
//                         'line-join': 'round',
//                         'line-cap': 'round'
//                     },
//                     'paint': {
//                         'line-color': '#89c',
//                         'line-width': 2
//                     }
//                 });
//             } catch (e) {
//                 console.log(e)
//             }
//         };
//     };
//     request.send();
// }

function callCurrentFlights() {
    var request = new XMLHttpRequest();
    request.open('GET', currentFlights, true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            let json = get_geojson(this.response)
            json.forEach((element) => {
                let bearing = 0

                if (plane_direction_data[element.properties.id] === undefined) {
                    plane_direction_data[element.properties.id] = element.geometry.coordinates;
                } else {
                    bearing  = getBearing(plane_direction_data[element.properties.id], element.geometry.coordinates);
                    console.log(element.properties.id, [plane_direction_data[element.properties.id], element.geometry.coordinates], bearing)
                    plane_direction_data[element.properties.id] = element.geometry.coordinates;
                }
                setMarkerData(element, bearing)
            });
        }
    };
    request.send();
}

function get_geojson(resp) {
    return JSON.parse(resp);
};

function setMarkerData(data, bearing=270) {
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
    .setRotation(bearing)
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

setIntervalAndExecute(main, 11000);









