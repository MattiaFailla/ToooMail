(function ($) {
    'use strict';

    $(document).on('ready', function () {
        // -----------------------------
        //  Testimonial Slider
        // -----------------------------
        $('.testimonial-slider').owlCarousel({
            loop:true,
            margin:20,
            dots:true,
            autoplay:true,
            responsive:{
                0:{
                    items:1
                },
                400:{
                    items:1
                },
                600:{
                    items:1
                },
                1000:{
                    items:2
                }
            }
        });
        // -----------------------------
        //  Story Slider
        // -----------------------------
        $('.about-slider').owlCarousel({
            loop:true,
            margin:20,
            dots:true,
            autoplay:true,
            items : 1
        });
        // -----------------------------
        //  Quote Slider
        // -----------------------------
        $('.quote-slider').owlCarousel({
            loop:true,
            autoplay:true,
            items : 1
        });
        // -----------------------------
        //  On Click Smooth scrool
        // -----------------------------
         $('.scrollTo').on('click', function(e) {
             e.preventDefault();
             var target = $(this).attr('href');
             $('html, body').animate({
               scrollTop: ($(target).offset().top)
             }, 500);
          });
        // -----------------------------
        //  Client Slider
        // -----------------------------
        $('.client-slider').owlCarousel({
            loop:true,
            autoplay:true,
            margin: 50,
            responsive:{
                0:{
                    items:1,
                    dots:false
                },
                400:{
                    items:2,
                    dots:false
                },
                600:{
                    items:2,
                    dots:false
                },
                1000:{
                    items:4
                }
            }
        });
        // -----------------------------
        //  Video Replace
        // -----------------------------
        $('.video-box i').click(function() {
            var video = '<iframe allowfullscreen src="' + $(this).attr('data-video') + '"></iframe>';
            $(this).replaceWith(video);
        });
        // -----------------------------
        //  Count Down JS
        // -----------------------------
        $('#simple-timer').syotimer({
            year: 2018,
            month: 5,
            day: 9,
            hour: 20,
            minute: 30
        });
        // -----------------------------
        //  Google Map
        // -----------------------------

        function initialize() {
            var styleArray = [];

            var myLatLng = {lat: 52.188933, lng: 33.083869};

            var mapOptions = {
                zoom: 7,
                scrollwheel: false,
                center: new google.maps.LatLng(52.188933, 33.083869),
                styles: styleArray
            };

            var map = new google.maps.Map(document.getElementById('googleMap'), mapOptions);
            
            var marker = new google.maps.Marker({
                position: myLatLng,
                map: map,
                title: 'Nexa'
            });
        }
        var mapId = $('#googleMap');
        if (mapId.length) {
            google.maps.event.addDomListener(window, 'load', initialize);
        }

    });

})(jQuery);