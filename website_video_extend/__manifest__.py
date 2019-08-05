# -*- coding: utf-8 -*-

{
    'name': 'Website Video',
    'category': 'Website',
    'sequence': 5,
    'summary': 'Add Videos in Website',
    'version': '1.3',
    'author': 'Atharva System',
    'support': 'support@atharvasystem.com',
    'website' : 'https://www.atharvasystem.com',
    'license' : 'OPL-1',
    'description': """
        """,
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets_backend.xml',  
        'views/product_video_view.xml',
        'views/templates.xml'
    ],
    'currency': 'EUR',
    'installable': True,
    'application': True,
}
