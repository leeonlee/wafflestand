function follow(id_in, button) {	
	$.getJSON("/follow/",{id:id_in, follow:button.value}, function(result){
		//alert("Successful?: " + result['success']);
	});
	button.value = (button.value == "Follow") ? "Unfollow" : "Follow";
	$(button).toggleClass('btn-warning');
	$(button).toggleClass('btn-success');
}
