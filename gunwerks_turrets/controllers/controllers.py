# -*- coding: utf-8 -*-
from odoo import http

# class GunwerksTurrets(http.Controller):
#     @http.route('/gunwerks_turrets/gunwerks_turrets/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gunwerks_turrets/gunwerks_turrets/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gunwerks_turrets.listing', {
#             'root': '/gunwerks_turrets/gunwerks_turrets',
#             'objects': http.request.env['gunwerks_turrets.gunwerks_turrets'].search([]),
#         })

#     @http.route('/gunwerks_turrets/gunwerks_turrets/objects/<model("gunwerks_turrets.gunwerks_turrets"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gunwerks_turrets.object', {
#             'object': obj
#         })