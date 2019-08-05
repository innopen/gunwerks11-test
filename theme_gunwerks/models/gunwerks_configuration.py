# -*- coding: utf-8 -*-

from odoo import fields, models


class BlogConfigure(models.Model):
    _name = 'blog.configure'

    name = fields.Char(string="Blog Slider Title", translate=True)
    blog_ids = fields.Many2many("blog.post", string="Blog Posts", domain=[('website_published','=',True)])
    active = fields.Boolean(string="Active", default=True)


class MultitabConfigure(models.Model):
    _name = 'multitab.configure'

    name = fields.Char(string="Group Name", translate=True)
    product_ids = fields.Many2many("product.template", string="Products", domain=[('website_published','=',True)])
    active = fields.Boolean(string="Active", default=True)
