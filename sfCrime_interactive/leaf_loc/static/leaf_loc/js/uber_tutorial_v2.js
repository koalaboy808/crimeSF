var userLatitude, userLongitude;
//var partyLatitude = 37.867475, partyLongitude = -122.274702;
//var partyLatitude, partyLongitude;
var geo = new google.maps.Geocoder;
var uberClientId = "nPN1DkEGRwvdl2S9FbhEOy8l5Um-8Js5"
  , uberServerToken = "SRsW_GXhu5CVmoO4eM1VLLRk6p6zkgFl-7XlrY2f" ;


function getGeocode(text) {
	geo.geocode({'address':text},function(results, status){
	    if (status == google.maps.GeocoderStatus.OK) {              
	        var myLatLng = results[0].geometry.location;

	        // Add some code to work with myLatLng    
	        console.log("hey");   
	        console.log(myLatLng.lat());
	        console.log(myLatLng.lng());  
	        var endlat = myLatLng.lat();
	        var endlng = myLatLng.lng();
	        dosecond(endlat,endlng)

	    } else {
	        alert("Geocode was not successful for the following reason: " + status);
	    }
	});
}


function dosecond(var1,var2){

navigator.geolocation.getCurrentPosition(function(position) {

	//dofirst();
	console.log("printing arguments");
	console.log(var1);
	console.log(var2);
	console.log("hello");
	//console.log(position);
    // Update latitude and longitude
    userLatitude = position.coords.latitude;
    userLongitude = position.coords.longitude;
    console.log("your latitude is" + userLatitude);
    console.log("your longitude is" + userLongitude);



    getEstimatesForUserLocation(userLatitude, userLongitude, var1, var2);


});

}


function getEstimatesForUserLocation(latitude,longitude, endlat, endlng) {
  $.ajax({
    url: "https://api.uber.com/v1/estimates/price",
    headers: {
        Authorization: "Token "  + uberServerToken
    },
    data: {
      start_latitude: latitude,
      start_longitude: longitude,
      end_latitude: endlat,
      end_longitude: endlng
    },
    success: function(result) {
      console.log(result);
    //   for(i = 0; i < result.prices.length; i++) {

    //             var x = document.createElement("div");
    // var t = document.createTextNode(result.prices[i].display_name + " " + result.prices[i].estimate);
    // //x.setAttribute("style", "background-color: grey;");
    // x.appendChild(t);
    // document.body.appendChild(x);
    // $('#price').html
                  $('#price1').html(result.prices[0].display_name + " " + result.prices[0].estimate);
                  $('#price2').html(result.prices[1].display_name + " " + result.prices[1].estimate);
                  $('#price3').html(result.prices[2].display_name + " " + result.prices[2].estimate);
                  $('#price4').html(result.prices[3].display_name + " " + result.prices[3].estimate);
                  $('#price5').html(result.prices[4].display_name + " " + result.prices[4].estimate);
                  $('#price6').html(result.prices[5].display_name + " " + result.prices[5].estimate);
              }
    
  });
}