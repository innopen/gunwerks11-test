odoo.define('product_review_management.review_js', function(require){
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
        if($.urlParam('review')=='True'){
            var msg = "Your review has been submitted successfully.";
            console.log($('.gn-product-details'));
            $('.gn-product-details').before('<div class="container"><div id="success-msg" class="alert alert-success">\
                                    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
                                    <strong></strong>'+msg+'</div></div>');
            window.history.replaceState(null, null, window.location.pathname);
        }
        else if($.urlParam('review')=='False'){
            var msg = "Sorry, Your review has not been submitted. Please try again.";
            $('.gn-product-details').before('<div class="container"><div id="success-msg" class="alert alert-danger">\
                                    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
                                    <strong></strong>'+msg+'</div></div>');
            window.history.replaceState(null, null, window.location.pathname);
        }
    });

    /*$(document).on("change", "#all_review_section .review-items-box li .add_like_dislike input[type='radio']", function(){
        var review_id = $(this).parents(".add_like_dislike").attr("data-review_id");
        $(this).parents(".add_like_dislike").find("input[name='like_dislike_" + review_id + "']:checked").siblings("label").find("i").addClass("checked");
        $(this).parents(".add_like_dislike").find("input[name='like_dislike_" + review_id + "']:not(':checked')").siblings("label").find("i").removeClass("checked");
        var like_dislike_value = $(this).parents(".add_like_dislike").find("input[name='like_dislike_" + review_id + "']:checked").val();
        var curr_element = $(this);
        ajax.jsonRpc("/product_review_like_dislike_update", 'call', {
            'review_id': review_id,
            'like_dislike_value': like_dislike_value,
        }).then(function(like_dislike_update){
            var add_count = curr_element.parents(".add_like_dislike").find("input[name='like_dislike_" + review_id + "'][value='" + like_dislike_value + "']").siblings("span");
            var subtract_count = curr_element.parents(".add_like_dislike").find("input[name='like_dislike_" + review_id + "'][value!='" + like_dislike_value + "']").siblings("span");
            if(like_dislike_update['plus_count'])
                add_count.html((parseInt(add_count.html()) + 1).toString());
            if(like_dislike_update['minus_count'])
                subtract_count.html((parseInt(subtract_count.html()) - 1).toString());
        });
    });*/
});

