# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Sales Commission on Sales/Invoice/Register Payment based on Configuration.",
    "author" : "BrowseInfo",
    "version" : "11.0.1.2",
    "depends" : ['base' , 'sale', 'sale_stock', 'sale_margin'],
    "summary" : "Sales Commission based on Partner, Product, Product Category and Margin calculated on Sales/Invoice/Register Payment",
    "description": """
    this module calculates sales commission on invoice , Sales Commission based on Product category, Product, Margin
    Sales Commission on Invoice
    Sales Commission on Sales
    Sales Commission on Register Payment
    Sales Commission on Invoice Payment
    Sales Commission on Payment
    Sales Commission based on Product
    Sales Commission based on Product Category
    Sales Commission based on Margin
    Sales Commission based on Partner
    Sales Commission Based Invoice
    Sales Commission Based Sales
    Sales Commission Based Register Payment
    Sales Commission Based Invoice Payment
    Sales Commission based Payment
    Agent Commission on Invoice
    Agent Commission on Sales
    Agent Commission on Register Payment
    Agent Commission on Invoice Payment
    Agent Commission on Payment
    Agent Commission based Invoice
    Agent Commission based Sales
    Agent Commission based Register Payment
    Agent Commission based Invoice Payment
    Agent Commission based Payment
    sales commision on invoice
    Sales commision on Sales
    Sales commision on Register Payment
    Sales commision on Invoice Payment
    Sales commision on Payment
    Sales commision based on Product
    Sales commision based on Product Category
    Sales commision based on Margin
    Sales commision based on Partner
    Sales commision Based Invoice
    Sales commision Based Sales
    Sales commision Based Register Payment
    Sales commision Based Invoice Payment
    Sales commision based Payment
    Agent commision on Invoice
    Agent commision on Sales
    Agent commision on Register Payment
    Agent commision on Invoice Payment
    Agent commision on Payment
    Agent commision based Invoice
    Agent commision based Sales
    Agent commision based Register Payment
    Agent commision based Invoice Payment
    Agent commision based Payment


    """,
    "website" : "www.browseinfo.in",
    "price": 69,
    "currency": 'EUR',
    "data" :[
        'security/sales_commission_security.xml',
        'security/ir.model.access.csv',
        'account/account_invoice_view.xml',
        'commission_view.xml',
        'base/res/res_partner_view.xml',
        'sale/sale_config_settings.xml',
        'sale/sale_view.xml',
        'report/commission_report.xml',
        'report/sale_inv_comm_template.xml'
    ],
    "auto_install": False,
    "installable": True,
    "images":['static/description/Banner.png'],
    'live_test_url':'https://youtu.be/4BlRGFqPiO8',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
