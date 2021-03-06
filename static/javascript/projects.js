var totalPictures = 0

function popupPortpholio(i, callback){
	if(i == totalPictures){
		i = 0;
	}else if(i == -1){
		i = totalPictures-1;
	}
	$clicked = $('#portImage-'+i);
	$('#popupPortpholio .photo-counter').html(i+1);
	$('#popupPortpholio img').attr("src", $clicked.data('image'));
	$('#popupPortpholio .flickr-url').attr("href", $clicked.data('url'));
	$('#popupPortpholio .photoleft').data('next', i-1);
	$('#popupPortpholio .photoright').data('next', i+1);
	if (callback){
		$('#popupPortpholio img').on('load', callback);
	}
}


$(document).ready(function(){
	$('#view-all-projects-btn').click(function(){
		$('#all-projects-display').slideToggle('fast');
    $(this).find('i').toggle();
	});

	$(document).foundation({
        orbit: {
            animation: 'fade',
            timer: true,
            timer_speed: 4000,
            timer_paused_class: 'slider-pause',
            slide_number: false,
            pause_on_hover: false,
            animation_speed: 1000,
            navigation_arrows: false,
            variable_height: false,
            bullets: false
        }
    });
    $("div.lazy").lazyload({
       effect : "fadeIn",
       threshold : 200
   	});

   	totalPictures = parseInt($('#popupPortpholio .photo-counter').data('total'));

   	$('.portpholio-image').each(function(i){
   		console.log('qwe')
		$(this).data('index', i);
		$(this).attr('id','portImage-'+i);
		$(this).click(function(){
			popupPortpholio($(this).data('index'), function(){
				$('#popupPortpholio').finish().fadeIn('fast');
			});
		});
	});

	$('#popupPortpholio .photoleft').click(function(){
		$('#popupPortpholio img').finish().fadeOut('fast', function(){
			popupPortpholio($('#popupPortpholio .photoleft').data('next'), function(){
				$('#popupPortpholio img').finish().fadeIn('fast');
			});
		});
	});

	$('#popupPortpholio .photoright').click(function(){
		$('#popupPortpholio img').finish().fadeOut('fast', function(){
			popupPortpholio($('#popupPortpholio .photoright').data('next'), function(){
				$('#popupPortpholio img').finish().fadeIn('fast');
			});
		});
	});

	$('#popupPortpholio .photoclose').click(function(){
		$('#popupPortpholio').finish().fadeOut('fast');
	});

	$('#popupPortpholio .centered').click(function(e){
		$('#popupPortpholio').finish().fadeOut('fast');
	});

	$('#view-all-pictures-btn').click(function(){
		$('#images-container').slideToggle();
    $(this).find('i').toggle();
	});
});