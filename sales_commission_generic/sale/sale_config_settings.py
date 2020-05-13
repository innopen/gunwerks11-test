# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class sale_configuration_settings(models.TransientModel):
    _inherit = "res.config.settings"

    commission_configuration = fields.Selection([('sale_order', 'Commission based on sales order'),
                                        ('invoice', 'Commission based on invoice'),
                                        ('payment', 'commission based on payment')
                                       ],string='Generate Commision Entry Based On ',default='payment')

    commission_discount_account = fields.Many2one('account.account',domain=[('user_type_id', '=', 'Expenses')],
                                                  string="Commission Account")

    def get_values(self):
        res = super(sale_configuration_settings, self).get_values()
        commission_configuration = self.env['ir.config_parameter'].sudo().get_param('sales_commission_generic.commission_configuration')
        commission_discount_account= int(self.env['ir.config_parameter'].sudo().get_param('sales_commission_generic.commission_discount_account'))
        res.update(
            commission_configuration = commission_configuration,
            commission_discount_account = commission_discount_account
        )
        return res

    def set_values(self):
        super(sale_configuration_settings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sales_commission_generic.commission_configuration', self.commission_configuration)
        self.env['ir.config_parameter'].sudo().set_param('sales_commission_generic.commission_discount_account', self.commission_discount_account.id)
