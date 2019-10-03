# -*- coding: utf-8 -*-
{
    'name': "gunwerks_turrets",

    'summary': """
        Module to create engravable scope turrets""",

    'description': """
        
    """,

    'author': "AndrewDHastings",
    'website': "http://www.AndrewDHastings.com",
    'license': 'Other proprietary',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    #'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','website','sale','mrp','gunwerks_ballistics'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

   'application': True,
}