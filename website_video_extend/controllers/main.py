# -*- coding: utf-8 -*-

import odoo
from odoo import fields, http, _
from odoo.http import request


class WebsiteForum(http.Controller):

    @http.route('/shop/get_content_delivery_video_urls', type='json', auth='public', website=True)
    def get_content_delivery_video_urls(self, src=None, **kwargs):
        website = request.website
        if not website.cdn_activated:
            return src
        if src and website.cdn_activated:
            src = website.get_cdn_url(src)
        return src

 
