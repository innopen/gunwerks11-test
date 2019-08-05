# -*- coding: utf-8 -*-

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    service_contact_number = fields.Char(string='Service Contact Number', default='1-800-GUNWERKS')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    service_contact_number = fields.Char(string='Service Contact Number', related='website_id.service_contact_number', default='1-800-GUNWERKS')
