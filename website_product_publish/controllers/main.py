# -*- coding: utf-8 -*-

from odoo import http, fields, _
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class GunwerksWebsite(Website):

    @http.route(['/website/publish'], type='json', auth="public", website=True)
    def publish(self, id, object):
        values = {}
        Model = request.env[object]
        record = Model.browse(int(id))
        if object == 'product.template' or object == 'product.product':
            if request.env.user.has_group('website_product_publish.group_website_manager'):
                res = super(GunwerksWebsite, self).publish(id=id, object=object)
                values['record'] = res
                values['result'] = True
            else:
                values['record'] = record.website_published
                values['result'] = False
        else:
            res = super(GunwerksWebsite, self).publish(id=id, object=object)
            values['record'] = res
            values['result'] = True
        return values

