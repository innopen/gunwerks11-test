# -*- coding: utf-8 -*-
{
    'name': 'Event Reviews',
    'category' : 'Website',
    'summary': """
        Online event reviews""",
    'license' : 'OPL-1',
    'version': '1.1',
    'author': 'Atharva System',
    'website': 'https://www.atharvasystem.com',
    'support': 'support@atharvasystem.com',
    'description': """
    Online event reviews
    """,
    'depends' : ['theme_gunwerks'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/assets.xml',
        'views/views.xml',
        'views/template.xml'
    ],
    'installable': True,
    'application': True,
}