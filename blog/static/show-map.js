const url = 'http://127.0.0.1:5000/aviation/api';
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
    var request = new XMLHttpRequest();
    // make a GET request to parse the GeoJSON at the url
    request.open('GET', url, true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            let json = get_geojson(this.response)
            json.forEach(element => {
                setMarkerData(element)
                console.log("LINE 24: ", element)
                try {
                    console.log("LINE 26: ", element.geometry.coordinates)
                    map.addSource(element.properties.id, {
                        'type': 'geojson',
                        'data': {
                            'type': 'Feature',
                            'properties': {},
                            'geometry': {
                                'type': 'LineString',
                                'coordinates': element.geometry.coordinates
                            }
                        }
                    });
                    map.addLayer({
                        'id': element.properties.id,
                        'type': 'line',
                        'source': element.properties.id,
                        'layout': {
                            'line-join': 'round',
                            'line-cap': 'round'
                        },
                        'paint': {
                        'line-color': '#888',
                        'line-width': 8
                        }
                    }); 
                } catch (error) {
                    console.log(error)
                };
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
    MKE: ${data.properties.model},
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









