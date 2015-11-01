var initializeSwiper = function() {

  var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        paginationClickable: true,
        spaceBetween: 30,
        centeredSlides: true,
        //autoplay: 5000,
        autoplayDisableOnInteraction: false,
         onSlideChangeStart: function(swiper) {
          swiper.slides.each(function(slide,i){
          $(slide).hide();

          });
          $(swiper.slides[swiper.activeIndex])
          .find('.content').toggle(0).fadeIn(1500);
        }
    });
};

var initBackToTop = function() {
  // hide #back-top first
  $("#back-top").hide();
  
  // fade in #back-top
  $(function () {
    $(window).scroll(function () {
      if ($(this).scrollTop() > 100) {
        $('#back-top').fadeIn();
      } else {
        $('#back-top').fadeOut();
      }
    });

    // scroll body to 0px on click
    $('#back-top a').click(function () {
      $('body,html').animate({
        scrollTop: 0
      }, 800);
      return false;
    });
  });

}
$(document).ready(function() {

  initBackToTop();
});
