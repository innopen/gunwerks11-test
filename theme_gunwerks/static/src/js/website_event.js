odoo.define('theme_gunwerks.website_event', function(require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;

    ajax.loadXML('/theme_gunwerks/static/src/xml/global_popup.xml', qweb);

    var snippet_animation = require('website.content.snippets.animation');

    snippet_animation.registry.form_builder_send = snippet_animation.registry.form_builder_send.extend({
        selector: '.s_website_form',
        start: function() {
            var self = this;
            this._super();
        },

        update_status: function(status) {
            this._super(status);
            if (status == 'success') {
                var msg = "Form Successfully Submitted.";
                $('#myModal').modal('hide');
                $('.modal-backdrop').remove();
                $('#success_message').show();
                $('#success_message').html(msg)
                $("#success_message").delay(4000).fadeOut();
            }
        }
    });

    $(document).ready(function() {
        $(".form_lead_popup .chatter_btn").click(function() {
            $('#myModal').modal('hide');
            $('body').removeClass().removeAttr('style');
            $('.modal-backdrop').remove();
            if($('.o_livechat_button').is(":visible")){
                $('.o_livechat_button').addClass("chatOpen").trigger("click");
            }
            else{
                if($('.o_chat_window').length > 0){
                    if($('.o_chat_window').height() !== 34)
                        $('.o_livechat_button').addClass("chatOpen");
                    else
                        $('.o_livechat_button').removeClass("chatOpen");

                }
                if(!$('.o_livechat_button').hasClass('chatOpen'))
                    $('.o_chat_title').trigger("click");
            }
        });  

        $(document).on('show.bs.modal', '.form_lead_popup', function() {
            $(this).find(".modal-body #myform .global-form-left").remove();
            $(this).find(".modal-body #myform #o_website_form_result").empty();
            $(this).find(".modal-body #myform #submitForm").removeClass("disabled");
            var popup_content = $(qweb.render("theme_gunwerks.global_popup_data"));
            $(this).find(".modal-body #myform").prepend(popup_content);
        });

        $('.gn-selectbox').each(function () {
            if ( $(this).find('option:selected').length > 0){
                if (! $(this).children('option:first-child').is(':selected')) {
                    $('#filterClear').show();
                }
            }
        });

        $(".btn-modal").click(function() {
            var passedID = $(this).data('id'); //get the id of the selected event 
            $('input[name=event_info]').val(passedID); //set the id to the input on the modal
        });

        var maxLength = 254;

        $(".event-desc a").each(function() {
            var myStr = $(this).text();
            if ($.trim(myStr).length > maxLength) {
                var newStr = myStr.substring(0, maxLength);
                var removedStr = myStr.substring(maxLength, $.trim(myStr).length);
                $(this).empty().html(newStr);
                $(this).append(' <span class="learn-more">Learn More</span>');
            }
        });
        // $(".read-more").click(function(){
        //     $(this).siblings(".more-text").contents().unwrap();
        //     $(this).remove();
        // });

        $('form.js_event_filter select').on('change', function(event) {
            if (!event.isDefaultPrevented()) {
                event.preventDefault();
                $(this).closest("form").submit();
            }
        });

    });

});