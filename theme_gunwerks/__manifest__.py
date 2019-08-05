# -*- coding: utf-8 -*-

{
    'name': "Theme Gunwerks",
    'category': 'Theme/Ecommerce',
    'summary': """
        Theme Gunwerks""",
    'version': '1.3',
    'author': "Atharva System",
    'license': 'OPL-1',
    'description': """
        Theme Gunwerks""",
    'depends': ['base','website_sale_wishlist', 'website_blog', 'website_event', 'event_sale','crm','website_sale_comparison','website_sale_options'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/assets.xml',
        'views/views.xml',
        'views/website_menu_views.xml',
        'views/templates.xml',
        'views/megamenu_templates.xml',
        'views/snippets.xml',
        'views/dynamic_snippets.xml',
        'views/blog_configure_views.xml',
        'views/multitab_configure_views.xml',
        'views/event_templates.xml',
        'views/event_detail_templates.xml',
        'views/event_view.xml',
        'views/product_view.xml',
        'views/product_detail.xml',
        'views/product_template.xml',
        'views/checkout.xml',
        'views/blogpost.xml',
        'views/blogs.xml',
        'views/blog_list.xml'
    ],
    'installable': True,
    'application': True
}
