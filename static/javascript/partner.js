$(document).ready(function(){
	$('#partnerForm-btn').click(function(){
		$(this).parent().slideUp('fast',function(){
			$('#partner-form').slideDown('fast');
		});
	});
});