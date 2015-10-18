var initializeSwiper = function() {

  var mySwiper = new Swiper('.swiper-container', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,

    // If we need pagination
    pagination: '.swiper-pagination',

    // Navigation arrows
    nextButton: '.swiper-button-next',
    prevButton: '.swiper-button-prev',
    onSlideChangeStart: function(swiper) {
      swiper.slides.each(function(slide,i){
          $(slide).hide();

      });
      $(swiper.slides[swiper.activeIndex])
      .find('.content').toggle(0).fadeIn(1500);
    },
  });
};

$(document).ready(function() {

  initializeSwiper();

});
