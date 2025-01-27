document.addEventListener('DOMContentLoaded', function () {
    // Dynamically find the map object by looking for the global variable starting with 'map_'
    var map = Object.values(window).find(obj => obj instanceof L.Map);
    console.log('here is the map object', map);

    if (map) {
        map.on('click', function (e) {
            var lat = e.latlng.lat;
            var lon = e.latlng.lng;
            fetch(`/query_coords?lat=${lat}&lon=${lon}`)
                .then(response => {
                    if (! response.ok){
                      L.popup()
                        .setLatLng([lat, lon])
                        .setContent('Backend search failed!')
                        .openOn(map);
                      throw new Error('Backend search failed!');
                    }
                    return response.json();
                  })
                .then(data => {
                    let text = `Maximum wave height (meters): ${data.wave_height}<br>Observation's distance from click (kilometers): ${data.distance}`;
                    L.popup()
                      .setLatLng([data.lat, data.lon])
                      .setContent(text)
                      .openOn(map);
                });
        });
    } else {
        console.error('Map object not found!');
    }
});
