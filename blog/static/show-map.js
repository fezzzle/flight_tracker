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
        addSource(element.properties.id, element)
        // dct['icao24'] = element.properties.id
        // icao24.push(dct)
    });
    // console.log("LINE 22: ", icao24)
    return json
}


function addSource(id, data) {
    // try {
    //     map.loadImage(
    //         'https://upload.wikimedia.org/wikipedia/commons/1/1e/Airplane_silhouette.png',
    //         function(error, image) {
    //         if (error) throw error;
    //         map.addImage('plane', image);
    try {
        map.addSource(id, { type: 'geojson', data: data });
        map.addLayer({
            'id': id,
            'type': 'symbol',
            'source': id,
            'layout': {
                // 'icon-size': 0.07,
                // 'icon-image': 'plane',
                'icon-image': 'airport-15'
            }
        });
    } catch {
        console.log("Caught 'ID ALREADY EXISTS'")
    }
        
        // })
    // } catch (e) {
    //     // pass
    // }
}

function get_geojson(resp) {
    return JSON.parse(resp);
}


function main() {
    var request = new XMLHttpRequest();
    // make a GET request to parse the GeoJSON at the url
    request.open('GET', url, true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400) {
            json = utility(this.response)
            // console.log(json)
            // addMarker(json)
            json.forEach(element => {
                console.log("LINE69 :", element)
                map.getSource(element.properties.id).setData(element);
            });
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









