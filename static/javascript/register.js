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
   		console.log(stripe_pk);
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
		$form = $('#register-form');
		if($form.parsley().validate()){
			var registeredEvent = $form.data('event');
			var ticket = getTicketInfo(
			{
				'event_slug': registeredEvent,
				'ticket_id': $('#id_tickets').val()
			},
			function(ticket){
				var handler = getCheckoutHandler(
					$form.serialize(), registeredEvent, ticket.key);
				handler.open({
			        name: $form.data('title'),
			        description: ticket.name,
			        amount: ticket.price,
			        email: $('#id_email').val(),
			        currency: "cad",
			        opened: function() {
			          // $('.checkout-action .fa').addClass('hide');
			          // $('.checkout-action .fa-paper-plane').removeClass('hide');
			          // $('.checkout-action .text').text(strStripeInAction);
			        },
			        closed: function() {
			          // if ($('.checkout-action').hasClass('token-was-obtained')) {
			          //   $('.checkout-action .fa').addClass('hide');
			          //   $('.checkout-action .fa-spinner').removeClass('hide');
			          //   $('.checkout-action').addClass('waiting');
			          //   $('.checkout-action .text').text(strCompletingRegistration);
			          //   setTimeout(function(){
			          //     if ($('.checkout-action').hasClass('waiting')) {
			          //       $('.checkout-action .text').text(strPlsWait);
			          //       setTimeout(function(){
			          //         if ($('.checkout-action').hasClass('waiting')) {
			          //           $('.checkout-action .text').text(strSmallTalk);
			          //         }
			          //       }, 20000);
			          //     }
			          //   }, 5000);
			          // } else {
			          //   enabledFormControls(true);
			          //   restoreCheckoutButton();
			          // }
			        }
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