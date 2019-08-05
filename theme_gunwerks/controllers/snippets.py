# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteBlog(WebsiteBlog):
    @http.route('/blog/get_blog_content', type='http', auth='public', website=True)
    def get_blog_content(self, **kw):
        values = {'blog_collection': 0}
        if kw.get('blog_col_id'):
            collection_data = request.env['blog.configure'].browse(int(kw.get('blog_col_id')))
            values.update({'blog_collection':collection_data})
        return request.render("theme_gunwerks.blog_snippet_content", values)


class WebsiteSale(WebsiteSale):
    @http.route('/shop/get_product_content', type='http', auth='public', website=True)
    def get_product_content(self, **kw):
        values = {'product_collection': 0}
        if kw.get('prod_col_id'):
            prod_col_rec = request.env['multitab.configure'].browse(int(kw.get('prod_col_id')))
            values.update({'product_collection':prod_col_rec})
        return request.render("theme_gunwerks.product_slider_content", values)

    @http.route('/shop/get_filter_list', type='http', auth='public', website=True)
    def get_filter_list(self, **kw):
        values = {'category': None}
        if kw.get('category_id'):
            category = request.env['product.public.category'].browse(int(kw.get('category_id')))
            values.update({'category': category})
        return request.render("theme_gunwerks.category_filter_content", values)

    @http.route('/shop/get_products_table', type='http', auth='public', website=True)
    def get_products_table(self, **post):
        category_id = int(post.get('category_id'))
        values = {'products': False}
        if category_id and category_id != 0:
            domain = request.website.sale_product_domain()
            domain += [('public_categ_ids', 'child_of', int(category_id))]

            pricelist = request.website.get_current_pricelist()
            from_currency = request.env.user.company_id.currency_id
            to_currency = pricelist.currency_id
            compute_currency = lambda price: from_currency.compute(price, to_currency)

            filters = post.get('filters')
            filter_values = []
            if filters:
                filter_list = [x.strip() for x in filters.split(',') if x != '']
                filter_values = [[int(x) for x in v.split("-")] for v in filter_list if v]

            domain = self._get_filter_domain(search='', category=category_id, filter_values=filter_values)
            Product = request.env['product.template']
            products = Product.search(domain)
            if products:
                values.update({
                    'products' : products,
                    'compute_currency': compute_currency,
                    'get_attribute_value_ids': self.get_attribute_value_ids,
                    'is_image': post.get('is_image'),
                    'is_description': post.get('is_description'),
                })
            return request.render("theme_gunwerks.products_dynamic_table_content", values)
        return False
