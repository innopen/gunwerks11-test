odoo.define('event_review_management.event_review', function(require){
    'use strict';

    var ajax = require('web.ajax');

    $.urlParam = function(name){
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results==null) {
            return null;
        }
        return decodeURI(results[1]) || 0;
    }
    
    $(document).on("click", "#submit_review_section .add_ratings span.fa-star", function(){
        $(this).addClass("checked");
        $(this).prevAll("span.fa-star").addClass("checked")
        $(this).nextAll("span.fa-star").removeClass("checked");
        $(this).parent().siblings("input[name='rating_number']").val($(this).parent().find("span.fa-star.checked").length);
    });

    $(document).on("submit", "#post-review form", function(event){
        if($(this).find("div#submit_review_section div.add_ratings .fa.fa-star.checked").length == 0){
            $( "#error" ).html( '<div class="alert alert-danger fade in alert-dismissible"><a href="#" class="close" data-dismiss="alert" aria-label="close" title="close">×</a><strong>Error!</strong> Please provide your ratings!</div>' );
            event.preventDefault();
            return false;
        }
    });

    $(document).ready(function() {
        if($.urlParam('review-add')=='True'){
            var msg = "Your review has been submitted successfully.";
            $('.gn-ed-section').before('<div class="container"><div id="success-msg" class="alert alert-success">\
                                    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
                                    <strong></strong>'+msg+'</div></div>');
            window.history.replaceState(null, null, window.location.pathname);
        }
        else if($.urlParam('review-add')=='False'){
            var msg = "Sorry, Your review has not been submitted. Please try again.";
            $('.gn-ed-section').before('<div class="container"><div id="success-msg" class="alert alert-danger">\
                                    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
                                    <strong></strong>'+msg+'</div></div>');
            window.history.replaceState(null, null, window.location.pathname);
        }

        $('#event_testimonial').owlCarousel({
            loop:false,
            margin:0,
            navText: ['<span aria-label="Previous"></span>', '<span aria-label="Next"></span>'],
            nav:true,
            dots:false,
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:2
                },
                1000:{
                    items:3
                }
            }
        });
    });
});

