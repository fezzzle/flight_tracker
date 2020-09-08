const url = 'http://127.0.0.1:5000/aviation/api';


mapboxgl.accessToken = 'pk.eyJ1Ijoiam9obnNtb3RoIiwiYSI6ImNrZWEycnRrdjAyZzYyd3AwYml5MjBuaXAifQ.CJqLW89MSuqwH-ijHwx_0w';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [25, 58.6],
    zoom: 7
});

function main(response) {
    let icao24 = []
    let json = get_geojson(response)
    json.forEach(element => {
        let dct = {}
        addSource(element.properties.id, element)
        dct['icao24'] = element.properties.id
        icao24.push(dct)
        // console.log(icao24)
    });
    console.log(icao24)
    // return icao24
}


function addSource(id, data) {
    try {
        map.addSource(id, { type: 'geojson', data: data });
        map.addLayer({
            'id': id,
            'type': 'symbol',
            'source': id,
            'layout': {
                'icon-image': 'airport-15'
            }
        });
    } catch (e) {
        console.log("An error in addSource")
    }
        
        
}

function get_geojson(resp) {
    return JSON.parse(resp);
}

map.on('load', function() {
    var request = new XMLHttpRequest();
    window.setInterval(function() {
        // make a GET request to parse the GeoJSON at the url
        request.open('GET', url, true);
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                icao24 = main(this.response)
                json = get_geojson(this.response)
                json.forEach(element => {
                    map.getSource(element.properties.id).setData(element);
                });
            }
        };
        request.send();
    }, 10000);


});






