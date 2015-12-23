$(document).ready(function() {
	$(document).foundation();

    "use strict"; // Start of use strict

    var messageResponses = {
    	stripeConnectionFailure:'We could not connect to Stripe.'
    }

    function displayMessage(success, message){
    	if(success){
    		$(".success-messages").html(message);
    		$(".error-messages").html();
    	}else{
    		$(".success-messages").html();
    		$(".error-messages").html(message);
    	}
    }


    function getTicketInfo(postData, callback){
    	$.ajax({
			type: 'POST',
			url: '/ticket/',
			data: postData,
			success: function(data){
				callback(data)
			},
			error: function(data){
				console.log(data);
			},
		});
    }

   	function getCheckoutHandler(formData, registeredEvent, stripe_pk){
		if (typeof StripeCheckout == 'undefined') {
			return displayMessage(false, messageResponses.strCannotConnectToStripe);
		}
		return StripeCheckout.configure({
            key: stripe_pk,
            image: 'https://docs.djangoproject.com/s/img/small-fundraising-heart.png',
            // image: '/static/images/logo.png',
            token: function(token) {
                // if (token.id) {
                //   $('.checkout-action').addClass('token-was-obtained');
                // }
                formData += '&token_id='+token.id;
                console.log('tocekn');
                console.log(formData);
                // if (window.challenge_id) {
                //   formData.append("challenge_id", window.challenge_id);
                // }
                // formData.append("lang", lang);
                // var lang = document.documentElement.lang;
                $.ajax({
					type: 'POST',
					url: '/register/'+registeredEvent+'/',
					data: formData,
					success: function(data){
						console.log(data);
						// $('#partner-form').slideUp();
						// $('#form-response').addClass('success');
						// $('#form-response').slideDown();
					},
					error: function(data){
						console.log(data);
						// var message = jQuery.parseJSON(data.responseText).message;
						// $('#form-response').html(message);
						// $('#form-response').addClass('failure');
						// $('#form-response').slideDown();
						// $('#partnerForm-submit-btn').attr("disabled", false);
					},
				});
            }
        });
	}

	$('#register-submit').click(function(){
		if($('#register-submit').css('disabled')){
			return;
		}
		$form = $('#register-form');
		var formData = $form.serialize();
		if($form.parsley().validate()){
			// $('#register-submit').css('disabled', true);
			$('#register-submit').html('')
			$('#register-submit').append('<i class="fa fa-cog fa-spin fa-inverse fa-lg"></i>')
			var registeredEvent = $form.data('event');
			var ticket = getTicketInfo(
			{
				'event_slug': registeredEvent,
				'ticket_id': $('#id_tickets').val()
			},
			function(ticket){
				// var handler = getCheckoutHandler(
				// 	formData, registeredEvent, ticket.key);
				// handler.open({
			 //        name: $form.data('title'),
			 //        description: ticket.name,
			 //        amount: ticket.price,
			 //        email: $('#id_email').val(),
			 //        currency: "cad",
			 //        opened: function() {

			 //        },
			 //        closed: function() {
				// 		$('#register-submit').css('disabled', false);
				// 		$('#register-submit').empty();
				// 		$('#register-submit').html('Register');
			 //        }
		  //     	});
		  //
		      	$.ajax({
					type: 'POST',
					url: '/register/'+registeredEvent+'/',
					data: formData +'&token_id=tok_17JE0l48LGa2TH25uJBm2ka8',
					success: function(data){
						console.log(data);
						// $('#partner-form').slideUp();
						// $('#form-response').addClass('success');
						// $('#form-response').slideDown();
					},
					error: function(data){
						console.log(data);
						// var message = jQuery.parseJSON(data.responseText).message;
						// $('#form-response').html(message);
						// $('#form-response').addClass('failure');
						// $('#form-response').slideDown();
						// $('#partnerForm-submit-btn').attr("disabled", false);
					},
				});
			});
		}
	});


	// // Close Checkout on page navigation
	// $(window).on('popstate', function() {
	// handler.close();
	// });
 	// });

}); // End of use strict