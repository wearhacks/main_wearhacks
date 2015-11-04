$(document).ready(function() {

$('#toggle-navigation').on("click",function(){
  var $nav = $('.navbar-nav.navbar-right');
  if($(this).hasClass('hide-nav'))
  {
    $(this).removeClass('hide-nav');
    $nav.animate({"margin-right": "0px"});
    $(this).find('.fa').rotate(0);
    $(this).find('span').animate({'width':'0px','opacity':'0'});
  }
  else
  {
    $(this).addClass('hide-nav');
    $nav.animate({"margin-right": "-600px"});
    $(this).find('.fa').rotate(180);
    $(this).find('span').animate({'width':'60px','opacity':'1'});
  }
});

$("#signup").on("click",function(){
  $(this).closest('form').submit();
});
$( "#footer-signup" ).submit(function( event ) {
 
  // Stop form from submitting normally
  event.preventDefault();
 
  // Get some values from elements on the page:
  var $form = $( this ),
    email = $form.find( "input[name='email']" ).val(),
    url = $form.attr( "action" );
 
  // Send the data using post
  var posting = $.post( url, { email: email } );
 
  // Put the results in a div
  posting.done(function( data ) {
    console.log(data);
    $( "#success-message" ).empty().append( data.message );
    $('#success-modal').foundation('reveal', 'open');
  });
  posting.fail(function(data) {

    $( "#error-message" ).empty().append( data.responseJSON.message );
    $('#error-modal').foundation('reveal', 'open');
  });
});
  initializeSwiper();
   window.sr= new scrollReveal({
          reset: true,
          mobile: true
        });


});

jQuery.fn.rotate = function(degrees) {
    $(this).css({'-webkit-transform' : 'rotate('+ degrees +'deg)',
                 '-moz-transform' : 'rotate('+ degrees +'deg)',
                 '-ms-transform' : 'rotate('+ degrees +'deg)',
                 'transform' : 'rotate('+ degrees +'deg)'});
    return $(this);
};

$(function() {
  $(".right-off-canvas-toggle, .exit-off-canvas").click(function() {
    $(".top-bar").toggleClass("top-bar-close");
    $(".middle-bar").toggleClass("middle-bar-close");
    $(".bottom-bar").toggleClass("bottom-bar-close");
    $('#navigation-drop').fadeToggle(200);
    });
});