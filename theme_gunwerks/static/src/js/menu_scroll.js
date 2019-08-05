(function($) {
    "use strict";
    
    var GUN = {};
     
    /*--------------------
        * Smooth Scroll
    ----------------------*/
    GUN.HeaderScroll = function() {

    /*--------------------
        * Smooth Scroll
    ----------------------*/
    var thHeight = $(".navbar-default").height();
    var ssHeight = $(".sticky_sub_menu").height();
    if(!ssHeight)
        ssHeight = 0;
    $('.section_title_scn h3 a[href*="#"]:not([href="#"])').on('click', function() {
            var PathName = location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') || location.hostname == this.hostname;
            if (PathName) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top - ( thHeight + ssHeight ),
                    }, 1000);
                    return false;
                }
            }
        });

    }

    /*--------------------
        * Header Fixed
    ----------------------*/
    GUN.HeaderFixed = function() {
        if ($(window).scrollTop() >= 60) {
            $('.navbar-default').addClass('fixed-header');
        }
        else {
            $('.navbar-default').removeClass('fixed-header');
        }
    }

    // On Ready
    $(document).on("ready", function() {
        GUN.HeaderScroll();
    });

    // On Scroll
    $(window).on("scroll", function() {
        GUN.HeaderFixed();
    });

})(jQuery);