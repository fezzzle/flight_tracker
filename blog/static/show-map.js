// const url = 'http://127.0.0.1:5000/aviation/api';
// let GEO_DATA = [];



// mapboxgl.accessToken = 'pk.eyJ1Ijoiam9obnNtb3RoIiwiYSI6ImNrZWEycnRrdjAyZzYyd3AwYml5MjBuaXAifQ.CJqLW89MSuqwH-ijHwx_0w';
// let map = new mapboxgl.Map({
//     container: 'map',
//     style: 'mapbox://styles/mapbox/streets-v11',
//     center: [25, 58.6], // starting position [lng, lat]
//     zoom: 7
// });

// function get_geojson() {
    
//     let request = new XMLHttpRequest();
//     request.open('GET', url, true);
//     request.onload = function() {
//         if (this.status >= 200 && this.status < 400) {
//             var json = JSON.parse(this.response);  

//             // update the drone symbol's location on the map
//             json.forEach(element => {
//                 GEO_DATA.push(element);
//                 console.log(element)
//                 map.getSource('drone').setData(element);
//             });

//             GEO_DATA.forEach(item => {
//                 map.addSource('drone', { type: 'geojson', data: item });
//             });
//         }
//         map.addLayer({
//             'id': 'drone',
//             'type': 'symbol',
//             'source': 'drone',
//             'layout': {
//             'icon-image': 'airport-15'
//             }
//         });
//     };
//     request.send();
// }

// console.log(GEO_DATA)



 
//     // // var url = 'https://wanderdrone.appspot.com/';


//     map.on('load', function() {
//         window.setInterval(function() {
//             get_geojson()
//         }, 10000);

//     });


const url = 'http://127.0.0.1:5000/aviation/api';


mapboxgl.accessToken = 'pk.eyJ1Ijoiam9obnNtb3RoIiwiYSI6ImNrZWEycnRrdjAyZzYyd3AwYml5MjBuaXAifQ.CJqLW89MSuqwH-ijHwx_0w';
let map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [25, 58.6], // starting position [lng, lat]
    zoom: 7
});

function main(response) {
    let icao24 = []
    let json = get_geojson(response)
    // console.log("75: ", json)
    json.forEach(element => {
        let dct = {}
        addSource(element.properties.id, element)
        dct['icao24'] = element.properties.id
        icao24.push(dct)
        // console.log(icao24)
    });
    console.log(icao24[0])
    // return icao24
}


function addSource(id, data) {
    // console.log("ID INSIDE ADDSOURCE: ", id)
    // console.log("DATA INSIDE ADDSOURCE: ", data)
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

// var url = 'https://wanderdrone.appspot.com/';
map.on('load', function() {
    var request = new XMLHttpRequest();
    window.setInterval(function() {
        // make a GET request to parse the GeoJSON at the url
        request.open('GET', url, true);
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                icao24 = main(this.response)
                // console.log("LINE119", icao24)
                // console.log("LINE119", icao24)
                // console.log("LINE120", icao24[0]['geometry'])
                json = get_geojson(this.response)
                json.forEach(element => {
                    map.getSource(element.properties.id).setData(element);
                });
            }
        };
        request.send();
    }, 6000);


});






