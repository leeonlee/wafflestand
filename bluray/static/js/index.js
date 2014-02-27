function follow(id_in, button) {	
	$.getJSON("/follow/",{id:id_in, follow:button.value}, function(result){
		//alert("Successful?: " + result['success']);
	});
	button.value = (button.value == "Follow") ? "Unfollow" : "Follow";
	$(button).toggleClass('btn-warning');
	$(button).toggleClass('btn-success');
}

$(document).ready(function() {
	
	$('#loginmodal').on('shown.bs.modal', function(){
		$('#id_username').focus();
	});

	$('#login_form').submit(function() {
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
	$('#reset_form').submit(function() {
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: "/accounts/password/reset/",
			beforeSend: function(xhr){
				$('#reset-message').html("Please wait..");
			}
			
		}).done(function(response){
			$('#reset-message').html("Thank you. If an account exists for the provided email, you will receive further instructions to reset your password");
		});
		return false
	});
});


