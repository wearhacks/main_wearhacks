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
