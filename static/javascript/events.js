
var initializeSwiper = function() {

    var swiper = new Swiper('.swiper-container-images', {
        pagination: '.swiper-pagination',
        slidesPerView: 4,
        paginationClickable: true,
        spaceBetween: 30,
        freeMode: true
    });
};

$(document).ready(function() {

  initializeSwiper();
   window.sr= new scrollReveal({
          reset: true,
          mobile: true
        });

});