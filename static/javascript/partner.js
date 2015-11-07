$(document).ready(function(){
	$('#partnerForm-btn').click(function(){
		$(this).parent().slideUp('fast',function(){
			$('#partner-form').slideDown('fast');
		});
	});

	$('#partnershipForm').submit(function(e) {
		$('#form-response').slideUp();
		$('#form-response').removeClass('failure');
		$('#form-response').removeClass('success');
		$('#partnerForm-submit-btn').attr("disabled", true);
	    $.ajax({
			type: 'POST',
			url: '/partnerships/',
			data: $('#partnershipForm').serialize(),
			success: function(data){
					console.log(data);
					$('#partner-form').slideUp();
					$('#form-response').html(data.message);
					$('#form-response').addClass('success');
					$('#form-response').slideDown();
				},
			error: function(data){
					var message = jQuery.parseJSON(data.responseText).message;
					$('#form-response').html(message);
					$('#form-response').addClass('failure');
					$('#form-response').slideDown();
					$('#partnerForm-submit-btn').attr("disabled", false);
				},
		});
	    e.preventDefault();
	});
});