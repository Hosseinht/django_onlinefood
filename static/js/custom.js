let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: {'country': ['us', 'ir']},
        })
// function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    } else {
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    console.log(place.address_components)
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value
    // console.log(address)

    geocoder.geocode({'address': address}, function (results, status) {
        console.log("results: ", results)
        console.log("status: ", status)
        if (status === google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat()
            var longitude = results[0].geometry.location.lng()
            // console.log("lat: ", latitude)
            // console.log("lng: ", longitude)
            $('#id_latitude').val(latitude)
            // this will put the value of the latitude inside the field that has the id of id_latitude
            $('#id_longitude').val(longitude)
            $('#id_address').val(address)
        }
    })

    for (var i = 0; i < place.address_components.length; i++) {
        // loop through address components
        for (var j = 0; j < place.address_components[i].types.length; j++) {
            // loop through address types
            if (place.address_components[i].types[j] === 'country') {
                // get country
                $("#id_country").val(place.address_components[i].long_name)
            }
            if (place.address_components[i].types[j] === 'administrative_area_level_1') {
                // get state
                $("#id_state").val(place.address_components[i].long_name)
            }
            if (place.address_components[i].types[j] === 'locality') {
                // get city
                $("#id_city").val(place.address_components[i].long_name)
            }
            if (place.address_components[i].types[j] === 'postal_code') {
                // get postal code
                $("#id_postal_code").val(place.address_components[i].long_name)
            } else {
                // if there is no postal code make this field blank
                $("#id_postal_code").val("")
            }

        }
    }
}
