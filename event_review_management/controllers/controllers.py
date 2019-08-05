# -*- coding: utf-8 -*-

import werkzeug
from odoo import http
from odoo.http import request
from werkzeug import url_encode


class PostReview(http.Controller):
    @http.route('/event/post-review', type='http', auth='public', methods=['POST'], website=True)
    def postReview(self, **kw):
        if kw.get('message') and kw.get('name'):
            website_id = request.website.id
            rv_data = {
                'customer_id': request.env.user.partner_id.id,
                'customer_name': request.env.user.partner_id.name,
                'rev_rating': kw.get('rating_number'),
                'event_id': kw.get('event_id')
            }
            if kw.get('name'):
                rv_data['name'] = kw.get('name')
            if kw.get('message'):
                rv_data['rev_message'] = kw.get('message')
            review_id = request.env['event.review'].create(rv_data)
            return werkzeug.utils.redirect(request.httprequest.referrer + "?%s" % url_encode({
                'review-add': 'True' if review_id else 'False'
            }))