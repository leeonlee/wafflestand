function track(id_in, track_or_not) {	
	$.getJSON("/track/",{id:id_in, track:track_or_not}, function(result){
		alert("Successful?: " + result['success']);
	});
}
