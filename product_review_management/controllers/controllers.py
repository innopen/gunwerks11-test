# -*- coding: utf-8 -*-

import werkzeug
from odoo import http
from odoo.http import request
from werkzeug import url_encode


class PostReview(http.Controller):
    @http.route('/shop/post-review', type='http', auth='public', methods=['POST'], website=True)
    def postReview(self, **kw):
        if kw.get('message') and kw.get('name'):
            website_id = request.website.id
            rv_data = {
                'customer_id': request.env.user.partner_id.id,
                'customer_name': request.env.user.partner_id.name,
                'rev_rating': kw.get('rating_number'),
                'product_tmpl_id': kw.get('product_tmpl_id')
            }
            if kw.get('name'):
                rv_data['name'] = kw.get('name')
            if kw.get('message'):
                rv_data['rev_message'] = kw.get('message')
            review_id = request.env['product.review'].create(rv_data)
            return werkzeug.utils.redirect(request.httprequest.referrer + "?%s" % url_encode({
                'review': 'True' if review_id else 'False'
                }))
    
    @http.route('/product_review_like_dislike_update', type='json', auth='public', website=True)
    def postLikeDislike(self, **kw):
        ret = {}
        if kw['review_id'] and 'like_dislike_value' in kw:
            review_rec = request.env['product.review'].search([('id','=',int(kw['review_id']))])
            if review_rec:
                ret['plus_count'] = False
                ret['minus_count'] = False
                if kw['like_dislike_value'] == 'like':
                    if request.session.uid not in review_rec.like_count.ids:
                        review_rec.sudo().update({'like_count': [(4, request.session.uid)]})
                        ret['plus_count'] = True
                    if request.session.uid in review_rec.dislike_count.ids:
                        temp_list = review_rec.dislike_count.ids
                        temp_list.remove(request.session.uid)
                        review_rec.sudo().update({'dislike_count': [(2, request.session.uid)]})
                        ret['minus_count'] = True
                elif kw['like_dislike_value'] == 'dislike':
                    if request.session.uid in review_rec.like_count.ids:
                        temp_list = review_rec.like_count.ids
                        temp_list.remove(request.session.uid)
                        review_rec.sudo().update({'like_count': [(2, request.session.uid)]})
                        ret['minus_count'] = True
                    if request.session.uid not in review_rec.dislike_count.ids:
                        review_rec.sudo().update({'dislike_count': [(4, request.session.uid)]})
                        ret['plus_count'] = True
                else:
                    pass
        return ret