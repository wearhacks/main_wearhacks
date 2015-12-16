/**
 * Created by nadim54321 on 15-10-18.
 */

var initializeSwiper3d = function() {

     var swiper = new Swiper('#swiper-3d', {
        pagination: '#swiper-3d .swiper-pagination',
        effect: 'cube',
        grabCursor: true,
        cube: {
            shadow: true,
            slideShadows: true,
            shadowOffset: 20,
            shadowScale: 0.94
        }
    });
};

$(document).ready(function() {

  initializeSwiper3d();
});
