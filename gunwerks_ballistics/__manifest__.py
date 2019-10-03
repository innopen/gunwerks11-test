# -*- coding: utf-8 -*-
{
    'name': "gunwerks_ballistics",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "AndrewDHastings",
    'website': "http://www.AndrewDHastings.com",
    'license': 'Other proprietary',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ballistic_profiles.xml',
        'views/workspaces.xml',
        'views/templates.xml',
        'data/bullet_caliber.xml',
        'data/bullet_mfg.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

   'application': True,
}