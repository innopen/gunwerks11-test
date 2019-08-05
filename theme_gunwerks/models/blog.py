# -*- coding: utf-8 -*-

from odoo import fields, models, api

class BlogPostType(models.Model):
    _name = 'blog.post.type'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(default=True)


class BlogPost(models.Model):
    _inherit = 'blog.post'

    cover_properties = fields.Text(
        'Cover Properties',
        default='{"background-image": "url(/web/image/theme_gunwerks.gunwerks_blog_post_cover)", "background-color": "oe_black", "opacity": "0.0", "resize_class": "cover container-fluid cover_full"}')

    author_avatar = fields.Binary(
        related='author_id.image_medium', string="Avatar")
    is_featured = fields.Boolean(
        name='Featured Blog', string='Featured Blog?', copy=False)
    blog_type = fields.Many2one(
        'blog.post.type', string='Blog type', store=True)

    def get_featured_blog(self, blog_id=None):
        blog = None
        if blog_id:
            blog = self.env["blog.post"].search(
                [('blog_id', '=', blog_id), ('is_featured', '=', True), ('website_published', '=', True)], limit=1, order='post_date desc')
        else:
            blog = self.env["blog.post"].search(
                [('is_featured', '=', True), ('website_published', '=', True)], limit=1, order='post_date desc')
        return blog

    def get_podcast_blog(self):
        blog_podcast_type = self.env.ref(
            'theme_gunwerks.gunwerks_blog_post_type_2').id
        blog = self.env["blog.post"].search(
            [('blog_type', '=', blog_podcast_type), ('website_published', '=', True)], limit=1, order='post_date desc')
        return blog

    def get_tv_blog(self):
        blog_tv_type = self.env.ref(
            'theme_gunwerks.gunwerks_blog_post_type_3').id
        blog = self.env["blog.post"].search(
            [('blog_type', '=', blog_tv_type), ('website_published', '=', True)], limit=1, order='post_date desc')
        return blog


class Blog(models.Model):
    _inherit = 'blog.blog'

    @api.multi
    def all_authors(self, min_limit=1):
        req = """
            SELECT
                p.blog_id, count(*), p.author_id
            FROM
                blog_post p
            WHERE
                p.blog_id in %s
            GROUP BY
                p.blog_id,
                p.author_id
            ORDER BY
                count(*) DESC
        """
        self._cr.execute(req, [tuple(self.ids)])
        author_by_blog = {i.id: [] for i in self}
        for blog_id, freq, author_id in self._cr.fetchall():
            if freq >= min_limit:
                author_by_blog[blog_id].append(author_id)

        BlogAuthor = self.env['res.partner']
        for blog_id in author_by_blog:
            author_by_blog[blog_id] = BlogAuthor.browse(
                author_by_blog[blog_id])
        return author_by_blog

    @api.multi
    def all_types(self, min_limit=1):
        req = """
            SELECT
                p.blog_id, count(*), p.blog_type
            FROM
                blog_post p
            WHERE
                p.blog_id in %s
            GROUP BY
                p.blog_id,
                p.blog_type
            ORDER BY
                count(*) DESC
        """
        self._cr.execute(req, [tuple(self.ids)])
        type_by_blog = {i.id: [] for i in self}
        for blog_id, freq, blog_type in self._cr.fetchall():
            if freq >= min_limit:
                type_by_blog[blog_id].append(blog_type)

        BlogType = self.env['blog.post.type']
        for blog_id in type_by_blog:
            type_by_blog[blog_id] = BlogType.browse(
                type_by_blog[blog_id])
        return type_by_blog
