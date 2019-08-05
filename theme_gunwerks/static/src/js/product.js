odoo.define('theme_gunwerks.product', function (require) {

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');

    var _t = core._t;


    $(document).on('click', '.gn-tooltip-attr', function(ev) {
        ev.preventDefault();
        ev.stopPropagation();

        var $form = $(ev.currentTarget).closest('form');
        var post = {};
        var url = false;
        var name = $(this).attr('name');

        if(name =='attribute'){
            post['attribute'] = $(this).attr('data-id');
            url = '/product/attribute/notes';
        }
        else if(name =='attribute_value'){
            post['attribute_val'] = $(this).attr('data-id');
            url = '/product/attributevalue/notes';
        }
        if(url){
            return ajax.jsonRpc(url, 'call', post).then(function (modal) {
                var $modal = $(modal);
                $modal.modal({keyboard: false});
                $modal.find('.modal-body > div').removeClass('container'); // retrocompatibility - REMOVE ME in master / saas-19
                $modal.insertAfter($form).modal();
                $modal.on('click', '.close', function () {
                    $modal.remove();
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                });
            });
        }
        else{
            return false;
        }
    });
});
