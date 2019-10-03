# -*- coding: utf-8 -*-
from odoo import http

# class GunwerksBallistics(http.Controller):
#     @http.route('/gunwerks_ballistics/gunwerks_ballistics/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gunwerks_ballistics/gunwerks_ballistics/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gunwerks_ballistics.listing', {
#             'root': '/gunwerks_ballistics/gunwerks_ballistics',
#             'objects': http.request.env['gunwerks_ballistics.gunwerks_ballistics'].search([]),
#         })

#     @http.route('/gunwerks_ballistics/gunwerks_ballistics/objects/<model("gunwerks_ballistics.gunwerks_ballistics"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gunwerks_ballistics.object', {
#             'object': obj
#         })