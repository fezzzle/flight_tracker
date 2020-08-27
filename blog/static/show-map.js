
mapboxgl.accessToken = 'pk.eyJ1Ijoiam9obnNtb3RoIiwiYSI6ImNrZWEycnRrdjAyZzYyd3AwYml5MjBuaXAifQ.CJqLW89MSuqwH-ijHwx_0w';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [25, 58.6], // starting position [lng, lat]
    zoom: 7
});

var url = 'https://wanderdrone.appspot.com/';
map.on('load', function() {
    var request = new XMLHttpRequest();
    window.setInterval(function() {
    // make a GET request to parse the GeoJSON at the url
    request.open('GET', url, true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            // retrieve the JSON from the response
            var json = JSON.parse(this.response);
            console.log(this.response)
            // {"geometry": {"type": "Point", "coordinates": [-89.39509694073094, 14.482296190921412]}, "type": "Feature", "properties": {}}
        
            // update the drone symbol's location on the map
            map.getSource('drone').setData(json);
        
            // fly the map to the drone's current location
            // map.flyTo({
            //     center: json.geometry.coordinates,
            //     speed: 0.1
            //     });
            }
        };
    request.send();
    }, 2000);
    
    map.addSource('drone', { type: 'geojson', data: url });
    map.addLayer({
    'id': 'drone',
    'type': 'symbol',
    'source': 'drone',
    'layout': {
    'icon-image': 'airport-15'
    }
    });
});
