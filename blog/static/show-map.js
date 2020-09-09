const url = 'http://127.0.0.1:5000/aviation/api';


mapboxgl.accessToken = 'pk.eyJ1Ijoiam9obnNtb3RoIiwiYSI6ImNrZWEycnRrdjAyZzYyd3AwYml5MjBuaXAifQ.CJqLW89MSuqwH-ijHwx_0w';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [25, 58.6],
    zoom: 7
});

function utility(response) {
    // let icao24 = []
    let json = get_geojson(response)
    console.log("LINE 15: ", json)
    json.forEach(element => {
        // let dct = {}
        // addIcon(element.properties.id, element)
        addMarker(element.properties.id, element)
        // dct['icao24'] = element.properties.id
        // icao24.push(dct)
    });
    return json
}

function get_geojson(resp) {
    return JSON.parse(resp);
}


function addMarker(id, data) {
    // create a DOM element for the marker
    var el = document.createElement('div');
    el.className = 'marker';
    el.style.backgroundImage = 'url(http://127.0.0.1:5000/static/marker.png)';
    el.style.width = data.properties.iconSize[0] + 'px';
    el.style.height = data.properties.iconSize[1] + 'px';
        
    el.addEventListener('click', function () {
    window.alert(data.properties.message);
    });
        
    // add marker to map
    new mapboxgl.Marker(el)
    .setLngLat(data.geometry.coordinates)
    .setRotation(90)
    .addTo(map);
}




// function addMarker(id, data) {
//     let el = document.createElement('div');
//     map.addSource(id, { type: 'geojson', data: data });
//     el.className = 'marker';

//     el.style.width = data.properties.iconSize[0] + 'px';
//     el.style.height = data.properties.iconSize[1] + 'px';

//     el.addEventListener('click', function() {
//     window.alert(data.properties.message);
//     });

//     new mapboxgl.Marker(el)
//         .setLngLat(data.geometry.coordinates)
//         .addTo(map);
// }
    


// function addIcon(id, data) {
//     try {
//         map.loadImage(
//             'http://127.0.0.1:5000/static/icon_default.png',
//             function(error, image) {
//             map.addImage('plane', image);
//             map.addSource(id, { type: 'geojson', data: data });
//             map.addLayer({
//                 'id': id,
//                 'type': 'symbol',
//                 'source': id,
//                 'layout': {
//                     'icon-size': 0.15,
//                     'icon-image': 'plane',
//                     // 'icon-image': 'airport-15'
//                 }
//             });        
//         })
//     } catch (e) {
//         // pass
//     }
// }


function main() {
    var request = new XMLHttpRequest();
    // make a GET request to parse the GeoJSON at the url
    request.open('GET', url, true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            json = utility(this.response);
            // json.forEach(element => {
            //     map.getSource(element.properties.id).setData(element);
            // });
        }
    };
    request.send();
}

function setIntervalAndExecute(fn, t) {
    map.on('load', function() {
        fn();
        return(setInterval(fn, t));
    });
}

setIntervalAndExecute(main, 10000);









