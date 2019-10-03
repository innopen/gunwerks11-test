odoo.define('theme_gunwerks.custom', function(require) {
    'use strict';

    // Equal Height
    /*function equalHeightProduct()
    {
        $('.row-level-1').each(function(){
            // Cache the highest
            var highestBox = 0;
          
            // Select and loop the elements you want to equalise
            $('.col-level-1', this).each(function(){
                // If this box is higher than the cached highest then store it
                if($(this).outerHeight() > highestBox) {
                    highestBox = $(this).outerHeight(); 
                }
            });  
            // Set the height of all those children to whichever was highest 
            $('.col-level-1 > .variant-box',this).outerHeight(highestBox);
        });
    }*/

    $(document).ready(function() {
        $('#event_detail_zoom').owlCarousel({
            loop:false,
            navText: ['<span aria-label="Previous"></span>', '<span aria-label="Next"></span>'],
            margin:0,
            nav:true,
            dots:false,
            responsive:{
                0:{
                    items:3
                },
                600:{
                    items:4
                },
                1000:{
                    items:5
                }
            }
        });

        $('#alt_product_slider').owlCarousel({
            loop:false,
            navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
            margin:20,
            nav:true,
            dots:false,
            responsive:{
                0:{
                    items:2
                },
                600:{
                    items:4
                },
                1000:{
                    items:6
                }
            }
        });

        $('#product_thumbs').owlCarousel({
            loop:false,
            navText: ['<span aria-label="Previous"></span>', '<span aria-label="Next"></span>'],
            margin:20,
            nav:true,
            dots:false,
            responsive:{
                0:{
                    items:4
                },
                600:{
                    items:4
                },
                1000:{
                    items:6
                }
            }
        });

        $(".quantity").on("keypress keyup blur",function (event) {
           $(this).val($(this).val().replace(/[^\d].+/, ""));
            if ((event.which < 48 || event.which > 57)) {
                event.preventDefault();
            }
        });


        $(".sub-images").click(function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            $('.event_detail_img').attr('src', this.src);
        }); 
        
        $(".hm-search .hm-search-hide").on("click", function(event) {
            $(".hm-search-box").toggleClass("hm-search-open");
            event.stopPropagation();
        });
        $(".hm-search-box").on("click", function(event) {
            event.stopPropagation();
        });

        $(document).on("click", function(event) {
            $(".hm-search-box").removeClass("hm-search-open");
        });

        // Mobile 
        $(".mm-mega-menu > a").after("<span class='mob_menu'></span>")
        $(".mm-cat-level-1 .cat-level-title").after("<span class='mob_menu'></span>")


        $(".mm-mega-menu .mob_menu").click(function() {
            $(this).parent('li').toggleClass("open-mob-menu");
            $(this).toggleClass("mob-menu-open");
        });

        $(".navbar-top-collapse .dropdown > .dropdown-toggle").after("<span class='mob_menu' data-toggle='dropdown' aria-expanded='false'></span>")


        // Event Filter Fixed
        $(document).on('click', '.event-filter-main .mob', function() {
            $(this).toggleClass('event-open');
            $('.event-filter-select').stop().slideToggle()
        })

        $(window).scroll(function() {
            // To Header
            if ($(window).scrollTop() >= 50) {
                $('body').addClass('fixed-header');
            } else {
                $('body').removeClass('fixed-header');
            }

            // for event scroll
            var headerHeight = $('header .navbar').height();
            var $ele = $(".js_event_filter");
            var $eleClass = $(".event-filter-main");
            if($ele.position() && $(window).scrollTop() >= $ele.position().top - headerHeight){
                $eleClass.addClass('fixed-event-filter');
            }
            else{
                $eleClass.removeClass('fixed-event-filter');
            }
        });


        //Sticky Sub Menu 
        $('.sticky-sub-menu-main').each(function() {
            var body =$("body");
            var s = $(".sticky-sub-menu-main");
            var pos = s.position();
            var hdrHeight = $('header .navbar').height()
            $(window).scroll(function() {
                var windowpos = $(window).scrollTop();
                if (windowpos >= pos.top + hdrHeight) {
                    body.addClass("f-sticky_sub_menu");
                } else {
                    body.removeClass("f-sticky_sub_menu");
                }
            });
        });

        var thHeight = $(".navbar-default").height();
        var ssHeight = $(".sticky_sub_menu").height();
        /*if(!ssHeight)
            ssHeight = 0;*/

        $(document).on("scroll", onScroll);
        $('.sticky-submenu a[href^="#"]').on('click', function(e) {
            e.preventDefault();
            $(document).off("scroll");
            $('.sticky-submenu a').each(function() {
                $(this).removeClass('active');
            })
            $(this).addClass('active');
            e.preventDefault();
            var hash = this.hash;
            $('html, body').stop().animate({
                //'scrollTop': $(hash).offset().top - ( thHeight + ssHeight ) + 2
                'scrollTop': $(hash).offset().top - ( ssHeight ) + 2
            }, 600, function() {
                //window.location.hash = hash;
                $(document).on("scroll", onScroll);
            });
        });

        function onScroll(event){
            var scrollPos = $(document).scrollTop();
            $('.sticky-submenu a').each(function () {
                var currLink = $(this);
                var refElement = $(currLink.attr("href"));
                var ssHeight = $(".sticky_sub_menu").height();
                if (refElement.position() && (refElement.position().top - ssHeight) <= scrollPos && refElement.position().top + refElement.height() > scrollPos) {
                    $('.sticky-submenu a').removeClass("active");
                    currLink.addClass("active");
                }
                else{
                    currLink.removeClass("active");
                }
            });
        }

        // Header Height
        var HHeight = $('.navbar-static-top').height()
        $('header').css("height", HHeight);

        $(window).resize(function() {
            var HHeight = $('.navbar-static-top').height()
            $('header').css("height", HHeight);
        });

        $('.video-popup').magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false,
            disableOn: function() {
                if( $(window).width() < 600 ) {
                    return true;
                }
                return true;
            }
        });

        $(".share-story").click(function(e){
            $(this).next('.dropdown-media').show();
            e.stopPropagation();
        });

        $(".dropdown-media").click(function(e){
            e.stopPropagation();
        });

        $(document).click(function(){
            $(".dropdown-media").hide();
        });

        /* Product Variant Page Start */
        // START BIZZAPPDEV CUSTOMIZATION

        var row_container = $('.tab-pane.container.active').find('.row-level-1');
        if (!row_container.length) {
            row_container = $('.row-level-1')
        }
        if(row_container.length > 0) {
            var col_container = $('.tab-pane.container.active').find('.col-level-1');
            if (!col_container.length) {
                col_container = $('.col-level-1')
            }
            var offset = row_container.offset();
            var height = row_container.height();
            var width = row_container.width();
            var widthT = col_container.width();
        // OLD CODE
        // if($('.row-level-1').length > 0) {

        //     var offset = $('.row-level-1').offset();
        //     var height = $('.row-level-1').height();
        //     var width = $('.row-level-1').width();
        //     var widthT = $('.col-level-1').width();
        // END BIZZAPPDEV CUSTOMIZATION
            var top = offset.top + height + "px";
            var right = offset.left + "px";
            $('.tab-variant-in').css( {
               'width': width,
            });

            if($(window).width() > 991){
                $('.col-level-1:nth-child(5n+1) .tab-variant-in').css( {
                    'width': width,
                });
                $('.col-level-1:nth-child(5n+2) .tab-variant-in').css( {
                    'left': -(width / 5) + 'px',
                });
                $('.col-level-1:nth-child(5n+3) .tab-variant-in').css( {
                    'left': -(widthT * 2) + 'px',
                });
                $('.col-level-1:nth-child(5n+4) .tab-variant-in').css( {
                    'left': -(widthT * 3) + 'px',
                });
                $('.col-level-1:nth-child(5n+5) .tab-variant-in').css( {
                    'left': -(widthT * 4) + 'px',
                });
            }
            else if($(window).width() > 767 && $(window).width() < 992 ){
                $('.col-level-1:nth-child(3n+2) .tab-variant-in').css( {
                    'left': -(width / 3) + 'px',
                });
                $('.col-level-1:nth-child(3n+3) .tab-variant-in').css( {
                    'left': -(widthT * 2) + 'px',
                });
            }
            else if($(window).width() > 400 && $(window).width() < 767 ){ // BIZZAPPDEV CUSTOMIZATION :: OLD(else {)
                $('.col-level-1:nth-child(2n+2) .tab-variant-in').css( {
                    'left': -(width / 2) + 'px',
                });
            }
        }

        // level show hide
        $('.row-level-1').each(function (i, elem) {
            var $elem = $(this),
            $acpanel = $elem.find(".col-level-1 > .tab-variant-in"),
            $acsnav =  $elem.find(".col-level-1 > .variant-box > .variant-box-in");
            $acsnav.on('click', function () {
                if(!$(this).parent('.variant-box').parent('.col-level-1').hasClass("acco-active")){
                    var $this = $(this).parent('.variant-box').next(".acco-des");
                    $acsnav.parent('.variant-box').parent('.col-level-1').removeClass("acco-active");
                    $(this).parent('.variant-box').parent('.col-level-1').addClass("acco-active");
                    $acpanel.not($this).slideUp("easeInExpo");
                    var $variant = $(this).parent('.variant-box');
                    $variant.next().slideDown("easeOutExpo");
                    $('html,body').animate({ 
                        scrollTop: ($($variant).offset().top - 250)
                    }, 1000);
                }else{
                   $(this).parent('.variant-box').parent('.col-level-1').removeClass("acco-active");
                   $(this).parent('.variant-box').next().slideUp("easeInExpo");
                }
                return false;
            });
        });

        // Set selected value on Attribute Section
        var value_selected = [];
        var total_attributes = $("input[name=total_attributes]").val();

        var tab_attr_count = [];
        var tab_attr_value = {};
        $('input[name^="p_t_info_"]').each(function() {
            var attr_name = $(this).attr('name')
            tab_attr_count[attr_name] = parseInt($(this).val());
            tab_attr_value[attr_name] = {};
        });

        $(".variant-value").on('click', function(e){
            /* Get value of an attribute */
            var attribute_id = $(this).attr('id');
            var value = $(this).parent('.variant-box').find('.variant-title').text();
            var img = $(this).parent('.variant-box').find('.variant-img').find('.img').attr('src');
            var value_id = parseInt($(this).parent('.variant-box').find('.variant-title').attr('id').replace("val-",""));

            // Set Value in Lable
            var find_val = "attr-"+attribute_id;
            $('#'+find_val).val(value_id);
            $('.'+find_val).text(value);

            // Replace Value Image on level1
            var find_img = "img-"+attribute_id;
            $('.'+find_img).parent('.variant-box').find('.img').attr("src",img);

            // When value is selelected, change color
            $('#'+find_val).closest('.variant-box').find('.variant-title').addClass('attr-val-selected');

            var name = $(this).closest('.tab-pane').find('input[name^="p_t_info_"]').attr('name');
            tab_attr_value[name][attribute_id] = value_id;
            if ($(this).closest('fieldset').hasClass('required_config_attrib')) {
                tab_req_attr_value[name][attribute_id] = value_id;
            }
            if(tab_attr_count[name] === Object.keys(tab_req_attr_value[name]).length){
                $("a[href='#"+ name +"']").addClass('panel-completed');
            }

            if(total_attributes > 0 && total_attributes == $('a.panel-completed').length){
                $('.js_check_product').removeClass('disabled');
            }
            
            /* Add class for border*/
            $(this).closest('.col-sm-4').addClass('border-val').siblings().removeClass('border-val');

            /* Slide Up */
            $(this).closest('.tab-variant-in').slideUp("easeInExpo");
            $(this).closest('.tab-variant-in').parent().removeClass("acco-active");
        });

        // Tabs navigation with Next Prev buttons
        $('.btnNext').click(function(){
            $('.nav-tabs > .active').next('li').find('a').trigger('click');
        });

        $('.btnPrevious').click(function(){
            $('.nav-tabs > .active').prev('li').find('a').trigger('click');
        });
        /* Product Variant Page END */

        //  Share Products on social media
        $(".o_twitter, .o_facebook, .o_linkedin, .o_google").on('click', function(event){
            var url = '';
            var product_title_complete = $('#product_details > h1 > .prod-name').html().trim() || '';
            if ($(this).hasClass('o_twitter')){
                url = 'https://twitter.com/intent/tweet?tw_p=tweetbutton&text=Amazing product : '+product_title_complete+"! Check it live: "+window.location.href;
                console.log(url);
            } else if ($(this).hasClass('o_facebook')){
                url = 'https://www.facebook.com/sharer/sharer.php?u='+window.location.href;
            } else if ($(this).hasClass('o_linkedin')){
                url = 'https://www.linkedin.com/shareArticle?mini=true&url='+window.location.href+'&title='+product_title_complete;
            } else if ($(this).hasClass('o_google')){
                url = 'https://plus.google.com/share?url='+window.location.href;
            }
            window.open(url, "", "menubar=no, width=500, height=400");
        });

    }); //document ready end
});
