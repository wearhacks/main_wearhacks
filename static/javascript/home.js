var initializeSwiper = function() {
  var lastindex = -1;
  var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        paginationClickable: true,
        spaceBetween: 30,
        centeredSlides: true,
        //autoplay: 4000,
        autoplayDisableOnInteraction: false,
        onSlideChangeStart: function(swiper) {
          lastindex = swiper.activeIndex;
          $(swiper.slides[swiper.activeIndex])
          .find('.content').fadeIn(1500);
          console.log("toggle in "+ swiper.activeIndex);
        },
        onSlideChangeEnd: function(swiper) {
          swiper.slides.each(function(i,slide){
            if(i !== swiper.activeIndex) {
              $(slide).find('.content').fadeOut(0);
              console.log("toggle out " + i);
            }

          });
        },
    });
    if(swiper.slides) {
      swiper.slides.each(function(i,slide){
              if(i !== 0)
                $(slide).find('.content').fadeOut(0);
      });
    }
      
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
  $('#signup-newsletter').on('click',  function() {
     console.log('hel');
     $('#signup-modal').foundation('reveal', 'open');
});

});
