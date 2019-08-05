# -*- coding: utf-8 -*-

import json
from odoo import http, fields, _
from odoo.http import request
from datetime import date
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import PPG, PPR
from odoo.addons.website_blog.controllers.main import WebsiteBlog


class GunwerksWebsiteSale(WebsiteSale):

    def _get_filter_domain(self, search, category, filter_values):
        domain = request.website.sale_product_domain()
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike',
                                    srch), ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch), ('product_variant_ids.default_code', 'ilike', srch)]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if filter_values:
            attrib = None
            ids = []
            for value in filter_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('filter_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('filter_line_ids.value_ids', 'in', ids)]

        return domain

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        if product.is_gunwerks_template:
            product_context = dict(request.env.context,
                                   active_id=product.id,
                                   partner=request.env.user.partner_id)
            ProductCategory = request.env['product.public.category']

            if category:
                category = ProductCategory.browse(int(category)).exists()

            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split("-")]
                             for v in attrib_list if v]
            attrib_set = {v[1] for v in attrib_values}

            keep = QueryURL('/shop', category=category and category.id,
                            search=search, attrib=attrib_list)

            categs = ProductCategory.search([('parent_id', '=', False)])

            pricelist = request.website.get_current_pricelist()

            from_currency = request.env.user.company_id.currency_id
            to_currency = pricelist.currency_id
            compute_currency = lambda price: from_currency.compute(
                price, to_currency)

            if not product_context.get('pricelist'):
                product_context['pricelist'] = pricelist.id
                product = product.with_context(product_context)

            values = {
                'search': search,
                'category': category,
                'pricelist': pricelist,
                'attrib_values': attrib_values,
                'compute_currency': compute_currency,
                'attrib_set': attrib_set,
                'keep': keep,
                'categories': categs,
                'main_object': product,
                'product': product,
                'get_attribute_value_ids': self.get_attribute_value_ids,
            }
            return request.render("theme_gunwerks.new_product_page", values)
        else:
            return super(GunwerksWebsiteSale, self).product(product=product, category=category, search=search, **kwargs)

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res = super(GunwerksWebsiteSale, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post)
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        parent_categories = []
        if category:
            url = "/shop/category/%s" % slug(category)
            current_category = category
            while current_category.parent_id:
                parent_categories.append(current_category.parent_id)
                current_category = current_category.parent_id

            parent_categories.reverse()
            child_category_ids = request.env['product.public.category'].search(
                [('parent_id', '=', category.id)])

            filter_list = request.httprequest.args.getlist('filter')
            filter_values = [[int(x) for x in v.split("-")]
                             for v in filter_list if v]
            filter_ids = {v[0] for v in filter_values}
            filter_set = {v[1] for v in filter_values}

            domain = self._get_filter_domain(search, category, filter_values)

            Product = request.env['product.template']
            product_count = Product.search_count(domain)
            pager = request.website.pager(
                url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
            products = Product.search(domain, limit=ppg, offset=pager[
                                      'offset'], order=self._get_search_order(post))

            filter_dict = {}
            if products:
                for product in products:
                    if product.filter_line_ids:
                        for filters_id in product.filter_line_ids:
                            for dataid in filters_id.filter_id:
                                for datavalue in filters_id.value_ids:
                                    if dataid in filter_dict:
                                        filter_dict[dataid] += (datavalue)
                                    else:
                                        filter_dict[dataid] = (datavalue)
            final_filter_dict = {a:list(set(b)) for a, b in filter_dict.items()}
            res.qcontext.update({
                'filter_dict': final_filter_dict,
                'filter_values': filter_values,
                'filter_set': filter_set,
                'products': products,
                'search_count': product_count,
                'bins': TableCompute().process(products, ppg),
                'parent_categories': parent_categories,
            })
        else:
            child_category_ids = request.env[
                'product.public.category'].search([('parent_id', '=', False)])
        if child_category_ids:
            res.qcontext.update({
                'child_categories': child_category_ids,
            })
        return res


class GunwerksWebsiteBlog(WebsiteBlog):

    WebsiteBlog._blog_post_per_page = 9

    @http.route([
        '/blog/<model("blog.blog"):blog>',
        '/blog/<model("blog.blog"):blog>/page/<int:page>',
        '/blog/<model("blog.blog"):blog>/tag/<string:tag>',
        '/blog/<model("blog.blog"):blog>/tag/<string:tag>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def blog(self, blog=None, tag=None, page=1, **opt):
        date_begin, date_end, state = opt.get(
            'date_begin'), opt.get('date_end'), opt.get('state')
        published_count, unpublished_count = 0, 0

        BlogPost = request.env['blog.post']

        Blog = request.env['blog.blog']
        blogs = Blog.search([], order="create_date asc")

        # build the domain for blog post to display
        domain = []
        # retrocompatibility to accept tag as slug
        active_tag_ids = tag and [int(unslug(t)[1])
                                  for t in tag.split(',')] or []
        if active_tag_ids:
            domain += [('tag_ids', 'in', active_tag_ids)]
        if blog:
            domain += [('blog_id', '=', blog.id)]
        if date_begin and date_end:
            domain += [("post_date", ">=", date_begin),
                       ("post_date", "<=", date_end)]

        if request.env.user.has_group('website.group_website_designer'):
            count_domain = domain + \
                [("website_published", "=", True),
                 ("post_date", "<=", fields.Datetime.now())]
            published_count = BlogPost.search_count(count_domain)
            unpublished_count = BlogPost.search_count(domain) - published_count

            if state == "published":
                domain += [("website_published", "=", True),
                           ("post_date", "<=", fields.Datetime.now())]
            elif state == "unpublished":
                domain += ['|', ("website_published", "=", False),
                           ("post_date", ">", fields.Datetime.now())]
        else:
            domain += [("post_date", "<=", fields.Datetime.now())]

        blog_url = QueryURL('', ['blog', 'tag'], blog=blog,
                            tag=tag, date_begin=date_begin, date_end=date_end)

        # Changes for the filters START
        all_authors = []
        types = []
        selected = {'author': '', 'type': '', 'tags': ''}

        if blog:
            all_authors = blog.all_authors()[blog.id]
            types = blog.all_types()[blog.id]

        tags = opt.get('tags')
        if tags:
            selected['tags'] = int(tags)
            domain += [('tag_ids', 'in', int(tags))]
        blog_posts = BlogPost.search(domain, order="post_date desc")

        author = opt.get('author')
        if author:
            selected['author'] = int(author)
            blog_posts = blog_posts.filtered(
                lambda r: r.author_id.id == int(author))

        type_id = opt.get('type')
        if type_id:
            selected['type'] = int(type_id)
            blog_posts = blog_posts.filtered(
                lambda r: r.blog_type.id == int(type_id))
        # Changes for the filters END

        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=len(blog_posts),
            page=page,
            step=self._blog_post_per_page,
            url_args=opt,
        )
        pager_begin = (page - 1) * self._blog_post_per_page
        pager_end = page * self._blog_post_per_page
        blog_posts = blog_posts[pager_begin:pager_end]

        all_tags = blog.all_tags()[blog.id]

        # function to create the string list of tag ids, and toggle a given one.
        # used in the 'Tags Cloud' template.
        def tags_list(tag_ids, current_tag):
            tag_ids = list(tag_ids)
            if current_tag in tag_ids:
                tag_ids.remove(current_tag)
            else:
                tag_ids.append(current_tag)
            tag_ids = request.env['blog.tag'].browse(tag_ids).exists()
            return ','.join(slug(tag) for tag in tag_ids)

        featured_blog_cover_properties = None
        featured_blog = request.env['blog.post'].get_featured_blog(blog.id)
        if featured_blog:
            featured_blog_cover_properties = json.loads(
                featured_blog.cover_properties)

        values = {
            'blog': blog,
            'blogs': blogs,
            'main_object': blog,
            'tags': all_tags,
            'state_info': {"state": state, "published": published_count, "unpublished": unpublished_count},
            'active_tag_ids': active_tag_ids,
            'tags_list': tags_list,
            'blog_posts': blog_posts,
            'blog_posts_cover_properties': [json.loads(b.cover_properties) for b in blog_posts],
            'pager': pager,
            'nav_list': self.nav_list(blog),
            'blog_url': blog_url,
            'date': date_begin,
            'authors': all_authors,
            'types': types,
            'selected': selected,
            'featured_blog': featured_blog,
            'featured_blog_cover_properties': featured_blog_cover_properties,
        }
        response = request.render("website_blog.blog_post_short", values)
        return response

    @http.route(['/more_blog_post'], type="json", auth="public", website=True)
    def more_blog_post(self, **opt):

        BlogPost = request.env['blog.post'].search([("website_published", "=", True),("post_date", "<=", fields.Datetime.now())], limit=9, order="post_date desc")
        values = {
            'blog_posts': BlogPost,
            'blog_posts_cover_properties': [json.loads(b.cover_properties) for b in BlogPost],
        }
        return {'template': request.env.ref("theme_gunwerks.more_blog_post").render(values)}

    @http.route()
    def blog_post(self, blog, blog_post, tag_id=None, page=1, enable_editor=None, **post):
        response = super(GunwerksWebsiteBlog, self).blog_post(
            blog=blog, blog_post=blog_post, tag_id=tag_id, page=page, enable_editor=enable_editor, **post)
        BlogPost = request.env['blog.post']
        featured_blog_posts = BlogPost.search(
            [('blog_id', '=', blog.id), ('id', '!=', blog_post.id)], order="post_date desc", limit=3)
        if featured_blog_posts:
            response.qcontext.update({
                'featured_blogs': featured_blog_posts,
                'blog_posts_cover_properties': [json.loads(b.cover_properties) for b in featured_blog_posts],
            })
        return response

    @http.route([
        '/blog',
        '/blog/page/<int:page>',
    ], type='http', auth="public", website=True)
    def blogs(self, page=1, **post):
        res = super(GunwerksWebsiteBlog, self).blogs(page=page, **post)
        featured_blog_cover_properties = tv_blog_cover_properties = None
        featured_blog = request.env['blog.post'].get_featured_blog()
        get_podcast_blog = request.env['blog.post'].get_podcast_blog()
        get_tv_blog = request.env['blog.post'].get_tv_blog()
        if featured_blog:
            featured_blog_cover_properties = json.loads(
                featured_blog.cover_properties)

        if get_tv_blog:
            tv_blog_cover_properties = json.loads(
                get_tv_blog.cover_properties)

        res.qcontext.update({
            'get_podcast_blog': get_podcast_blog,
            'get_tv_blog': get_tv_blog,
            'featured_blog': featured_blog,
            'featured_blog_cover_properties': featured_blog_cover_properties,
            'tv_blog_cover_properties': tv_blog_cover_properties,
        })
        return res


class Gunbuilder(http.Controller):

    @http.route(['/product/attribute/notes'], type='json', auth="public", methods=['POST'], website=True)
    def get_tooltip_notes(self, **post):
        tooltip = False
        if post.get('attribute'):
            attribute = request.env['product.attribute'].browse(int(post.get('attribute')))
            if attribute:
                tooltip = attribute.tooltip_notes
        return request.env['ir.ui.view'].render_template("theme_gunwerks.gunwerks_tooltip", {'tooltip': tooltip})

    @http.route(['/product/attributevalue/notes'], type='json', auth="public", methods=['POST'], website=True)
    def get_value_tooltip_notes(self, **post):
        tooltip = False
        if post.get('attribute_val'):
            attribute_val = request.env['product.attribute.value'].browse(int(post.get('attribute_val')))
            if attribute_val:
                tooltip = attribute_val.tooltip_notes
        return request.env['ir.ui.view'].render_template("theme_gunwerks.gunwerks_tooltip", {'tooltip': tooltip})
