# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    author = fields.Boolean(string='Is an Author', default=False,
                               help="Check this box if this contact is an author. It can be selected in Blog.")
    author_profile = fields.Html(string="Author Profile", translate=True)

    instructor = fields.Boolean(string='Is an Instructor', default=False,
                               help="Check this box if this contact is an instructor. It can be selected in Event.")
    instructor_profile = fields.Html(string="Instructor Profile", translate=True)

