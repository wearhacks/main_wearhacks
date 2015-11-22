$(document).ready(function(){
	$('#viewAllProjectBtn').click(function(){
		$(this).slideUp('fast');
		$('#allProjectsDisplay').slideDown('fast');
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
});