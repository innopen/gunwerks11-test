# -*- coding: utf-8 -*-

from odoo import fields, models


class MegamenuContent(models.Model):
    _name='megamenu.content'
    
    name=fields.Char(string="Content Name", translate=True)
    active=fields.Boolean(string="Active", default=True)
    is_header=fields.Boolean(string="Header")
    is_footer=fields.Boolean(string="Footer")
    main_content_type=fields.Selection([('product_grid','Product Grid'),('product_list','Product Listing'),
                                        ('category_grid','Category Grid'),('category_list','Category Listing'),
                                        ('content','Content')], string='Content Type',translate=True)
    no_of_columns=fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6')],
                                   string="Number of Columns",translate=True)
    product_ids=fields.Many2many("product.template",string="Products", domain=[('website_published','=',True)])
    product_lable_color=fields.Char(string="Product Label Color")
    header_content=fields.Html(string="Header Content",translate=True)
    footer_content=fields.Html(string="Footer Content",translate=True)
    category_ids=fields.Many2many("product.public.category", string="Category", domain=['|',('parent_id','=',False),('parent_id.parent_id','=',False)])
    category_lable_color=fields.Char(string="Category Label Color")
    menu_content=fields.Html(string="Content", translate=True)
    
    
class WebsiteMenu(models.Model):
    _inherit="website.menu"
    
    is_mega_menu=fields.Boolean(string="Mega Menu")
    content_id=fields.Many2one("megamenu.content", string="Content")
    parent_id=fields.Many2one('website.menu', string='Parent Menu', index=True, ondelete="cascade",domain=[('is_mega_menu','=',False)])
