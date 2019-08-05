# -*- coding: utf-8 -*-
{
    'name': 'Advanced Product Reviews',
    'category' : 'Website',
    'summary': """
        A highly customizable product advanced reviews system simplifies making a purchase decision for your customers by reading online product reviews.""",
    'license' : 'OPL-1',
    'version': '1.1',
    'author': 'Atharva System',
    'website': 'https://www.atharvasystem.com',
    'support': 'support@atharvasystem.com',
    'description': """
    Advanced Product Reviews,
    ratings and reviews management,
    Website Product Review/Rating,
    Website: Product Review,
    Website Review Rating,
    Product Review and Rating,
	Website Review,
	Website Product Review,
	Products Review,
	Google Review,
	Review and rating,
	simple reviews, customer review ,  product review system , odoo reviews ratin ,  product reviews app ,  product reviews module 
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
    'images': ['static/description/advance-product-review.png'],
    'price': 25.00,
    'currency': 'EUR'
}