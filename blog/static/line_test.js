const url = 'http://127.0.0.1:5000/aviation/flight_data';

mapboxgl.accessToken = 'pk.eyJ1Ijoiam9obnNtb3RoIiwiYSI6ImNrZWEycnRrdjAyZzYyd3AwYml5MjBuaXAifQ.CJqLW89MSuqwH-ijHwx_0w';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [25, 58.6],
    zoom: 7
    // center: [-122.486052, 37.830348],
    // zoom: 15
});


function main() {
    var request = new XMLHttpRequest();
    // make a GET request to parse the GeoJSON at the url
    request.open('GET', url, true);
    request.onload = function() {
        let flights = []
        if (this.status >= 200 && this.status < 400) {
            let api_resp = JSON.parse(this.response)
            console.log(api_resp.flights[0].flight_data)
            let planeFlights = api_resp.flights[0].flight_data
            planeFlights.forEach((flight) => {
                flights.push(Array.from([flight.longitude, flight.latitude]))
            });
            map.addSource('route', {
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

        };
    };
    request.send();
}

map.on('load', function () {
    main()
});
