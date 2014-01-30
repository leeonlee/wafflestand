function track(id_in, button) {	
	$.getJSON("/track/",{id:id_in, track:button.value}, function(result){
		alert("Successful?: " + result['success']);
	});
	button.value = (button.value == "Track") ? "Untrack" : "Track";
	$(button).toggleClass('btn-warning');
	$(button).toggleClass('btn-success');
}
