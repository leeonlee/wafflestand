function track(id_in, button) {	
	$.getJSON("/track/",{id:id_in, track:button.value}, function(result){
		alert("Successful?: " + result['success']);
	});
	button.value = (button.value == "Track") ? "Untrack" : "Track";
	$(button).toggleClass('btn-warning');
	$(button).toggleClass('btn-success');
}

$(document).ready(function() {
	
	$('#login').click(function(){	
		$('#loginmodal').modal('show');
		$('#loginmodal').on('shown.bs.modal', function(){
			$('#id_username').focus()
		});
	});

	$('#loginform').submit(function() {
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: "/loginview/",
			success: function(response){
				if (response['success'] == 'success'){
					location.reload();
				} else if (response['success'] == 'validate'){
					$('#form-error').html("Check account's email");
				} else {
					$('#form-error').html("Invalid credentials");
				}
			}
		});
		return false
	});
});


