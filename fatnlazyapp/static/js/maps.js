// function initialize() {
//         var mapCanvas = document.getElementById('map');
//         var mapOptions = {
//           center: new google.maps.LatLng(44.5403, -78.5463),
//           zoom: 16,
//           mapTypeId: google.maps.MapTypeId.ROADMAP
//         };
//         var resultsMap = new google.maps.Map(mapCanvas, mapOptions);
//         var geocoder = new google.maps.Geocoder();
//         var parameters = location.search.substring(1);
//         var temp = parameters.split("=");
//         var address = temp[1];
//        geocoder.geocode({'address': address}, function(results, status)
//        {
//            if (status === google.maps.GeocoderStatus.OK)
//            {
//               resultsMap.setCenter(results[0].geometry.location);
//                var marker = new google.maps.Marker({
//                                map: resultsMap,
//                               position: results[0].geometry.location
//                              });
//             }
//             else
//             {
//               alert('Geocode was not successful for the following reason: ' + status);
//             }
//         });
//         }
var resultsMap;
var currentLat;
var currentLong;

function initialize() {

  var mapCanvas = document.getElementById('map');
  var mapOptions = {
    center: new google.maps.LatLng(44.5403, -78.5463),
    zoom: 16,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  resultsMap = new google.maps.Map(mapCanvas, mapOptions);

  if (navigator.geolocation) {
    var startPos;
    var geoOptions = {
      maximumAge: 5 * 60 * 1000,
      timeout: 10 * 1000
    }

    var geoSuccess = function(position) {
      startPos = position;
      lat = startPos.coords.latitude;
      lng = startPos.coords.longitude;
      currentLong = lng;
      currentLat =lat;
      var point = new google.maps.LatLng(lat, lng);
      resultsMap.setCenter(point);
      var markerImage = 'http://www.mapsmarker.com/wp-content/uploads/leaflet-maps-marker-icons/bar_coktail.png';
      var marker = new google.maps.Marker({
        map: resultsMap,
        position: point,
        title: "Current Location!!!",
        icon: markerImage
      });
    };
    
    var geoError = function(error) {
      console.log('Error occurred. Error code: ' + error.code);
      // error.code can be:
      //   0: unknown error
      //   1: permission denied
      //   2: position unavailable (error response from location provider)
      //   3: timed out
    };

    navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
  } else {
    alert('Geolocation is not supported for this Browser/OS version yet.');
  }

  document.getElementById("searchFood").onclick = searchFood;

  var input = (document.getElementById('newLocation'));
  var autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.bindTo('bounds', resultsMap);

  document.getElementById("changeLocation").onclick = searchPlace;
}

function searchPlace() {

  var geocoder = new google.maps.Geocoder();

  var addressBar = (document.getElementById('newLocation'));

  var address = addressBar.value;


  geocoder.geocode({
    'address': address
  }, function(results, status) {

    if (status === google.maps.GeocoderStatus.OK) {

      newLocation = results[0].geometry.location;
      currentLat = newLocation.lat();
      currentLong = newLocation.lng();

      // var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
      // var contentString = 'You are here';
      var markerImage = 'http://www.mapsmarker.com/wp-content/uploads/leaflet-maps-marker-icons/bar_coktail.png';
      
      // var infowindow = new google.maps.InfoWindow({
      // content: contentString
      // });

      var marker = new google.maps.Marker({
        position: newLocation,
        map: resultsMap,
        icon: markerImage
      });

       // marker.setMap(resultsMap);

      if ((!resultsMap.getBounds().contains(marker.getPosition()))) {
        resultsMap.setCenter(marker.getPosition());
      }
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });

}

function searchFood() {

  var cuisine = (document.getElementById('cuisine').value);

  $.ajax({
    type: "POST",
    url: "/get_results",
    data: { lat: currentLat, lng: currentLong, num_results : 10, keyword : cuisine}
  }).done(function(param) {
                           // do something
                          //  alert(param)
                           var myWindow = window.open("", "MsgWindow", "width=200, height=100");
                           myWindow.document.write(param);

                          });
}

google.maps.event.addDomListener(window, 'load', initialize);
