odoo.define('theme_gunwerks.WebsiteRoot', function (require) {
'use strict';

var websiteRootData = require('website.WebsiteRoot');

var WebsiteRoot = websiteRootData.WebsiteRoot.include({
    _onPublishBtnClick: function (ev) {
        ev.preventDefault();

        var self = this;
        var $data = $(ev.currentTarget).parents(".js_publish_management:first");
        this._rpc({
            route: $data.data('controller') || '/website/publish',
            params: {
                id: +$data.data('id'),
                object: $data.data('object'),
            },
        })
        .done(function (result) {
            if(result.result)
            {
                $data.toggleClass("css_unpublished css_published");
                $data.find('input').prop("checked", result.record);
                $data.parents("[data-publish]").attr("data-publish", +result.result ? 'on' : 'off');
            }
        })
        .fail(function (err, data) {
            return new Dialog(self, {
                title: data.data ? data.data.arguments[0] : "",
                $content: $('<div/>', {
                    html: (data.data ? data.data.arguments[1] : data.statusText)
                        + '<br/>'
                        + _.str.sprintf(
                            _t('It might be possible to edit the relevant items or fix the issue in <a href="%s">the classic Odoo interface</a>'),
                            '/web#return_label=Website&model=' + $data.data('object') + '&id=' + $data.data('id')
                        ),
                }),
            }).open();
        });
    }
});

return WebsiteRoot;
});
