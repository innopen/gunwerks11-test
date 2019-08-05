odoo.define('theme_gunwerks.web_event', function (require) {
'use strict';

var ajax = require('web.ajax');
var EventRegistrationForm = require('website_event.website_event');

$(document).on('click', '#loadmore', function(){
    $(this).addClass('disabled');
    return ajax.jsonRpc('/more_blog_post', 'call', {
    }).then(function(data) {
        $("div#moreblog").append(data.template);
    });
})

var EventDetail = EventRegistrationForm.include({
    on_click: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var $form = $(ev.currentTarget).closest('form');
        var $button = $(ev.currentTarget).closest('[type="submit"]');
        var post = {};
        $('#registration_form table').siblings('.alert').remove();
        $('#registration_form input[type=text]').each(function () {
            post[$(this).attr('name')] = $(this).val();
        });
        var tickets_ordered = _.some(_.map(post, function (value, key) { return parseInt(value); }));
        if (!tickets_ordered) {
            $('<div class="alert alert-info"/>')
                .text(_t('Please select at least one ticket.'))
                .insertAfter('#registration_form table');
            return $.Deferred();
        } else {
            $button.attr('disabled', true);
            return ajax.jsonRpc($form.attr('action'), 'call', post).then(function (modal) {
                var $modal = $(modal);
                $modal.modal({backdrop: 'static', keyboard: false});
                $modal.find('.modal-body > div').removeClass('container'); // retrocompatibility - REMOVE ME in master / saas-19
                $modal.insertAfter($form).modal();
                $modal.on('click', '.js_goto_event', function () {
                    $modal.modal('hide');
                    $button.prop('disabled', false);
                });
                $modal.on('click', '.close', function () {
                    $button.prop('disabled', false);
                });
            });
        }
    },
});

return EventDetail;
});
