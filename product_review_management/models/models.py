# -*- coding: utf-8 -*-

from odoo import models, tools, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError

class ProductReviewCategory(models.Model):
    _name = 'product.review.category'
    _description = 'Product Review Tags'

    name = fields.Char(string='Tag Name', required=True, translate=True)
    active = fields.Boolean(default=True, help="The active field allows you to hide the category without removing it.")


class ProductReview(models.Model):
    _name = "product.review"
    _rec_name = 'customer_name'
    _order = "is_published desc, crt_date desc"


    @api.model
    def _get_auto_published_setting(self):
        web_setting_rec = self.env['res.config.settings'].sudo().get_values()
        return web_setting_rec['direct_review_publishing_option'] if web_setting_rec.get('direct_review_publishing_option') else False

    @api.model
    def _default_customer(self):
        user_rec = self.env['res.users'].search([('id','=',self._uid)])
        return user_rec.name if user_rec else ''

    @api.onchange('customer_id')
    def onchange_default_customer(self):
        if self.customer_id:
            self.customer_name = self.customer_id.name

    @api.multi
    def website_publish_unpublish_button(self):
        self.ensure_one()
        return self.write({'is_published': not self.is_published})

    def _default_category(self):
        return self.env['product.review.category'].browse(self._context.get('category_id'))

    name = fields.Char(name='title', string='Title')
    rev_rating = fields.Selection(selection=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], name='revRating', string='Rating', default='1')
    rev_message = fields.Text(name='revMessage', string='Review')
    # like_count = fields.Many2many('res.users', 'like_review_user_rel', 'review_id', 'user_id', name='likeCount', string='Likes Count')
    # dislike_count = fields.Many2many('res.users', 'dislike_review_user_rel', 'review_id', 'user_id', name='dislikeCount', string='Dislikes Count')
    customer_id = fields.Many2one("res.partner", name='customerId', string="Customer")
    customer_name = fields.Char(name='customerName', string='Customer Name', default=_default_customer)
    # review_verified = fields.Boolean(name='reviewVerified', string='Review Verified', default=False)
    # admin_review = fields.Boolean(name='adminReview', string='Admin Response', default=False)
    # admin_comment = fields.Text(name='adminComment', string='Admin Comment', default='')
    crt_date = fields.Datetime(name='crtDate', string='Review Create Date')
    is_published = fields.Boolean(name='isPublished', string='Publish on the website', copy=False, default=_get_auto_published_setting)
    published_date = fields.Datetime(name='publishedDate', string='Published Date', default='')
    product_tmpl_id = fields.Many2one('product.template', name='productTemplId', string='Product')
    category_id = fields.Many2many('product.review.category', column1='review_id',
                                    column2='category_id', string='Tags', default=_default_category)

    @api.model
    def create(self, values):
        if 'rev_rating' in values and values['rev_rating']:
            if int(values['rev_rating']) < 1 or int(values['rev_rating']) > 5:
                raise UserError("The Review's rating should be a number between 1 and 5.")
        res = super(ProductReview, self).create(values)
        curr_website = self.env['website'].get_current_website()
        if curr_website:
            if curr_website.direct_review_publishing_option:
                res.update({'published_date': res.crt_date})
            else: 
                if values.get('is_published'):
                    values['published_date'] = fields.Datatime.now()
        return res

    @api.one
    def write(self, values):
        if values.get('rev_rating'):
            if int(values['rev_rating']) < 1 or int(values['rev_rating']) > 5:
                raise UserError("The Review's rating should be a number between 1 and 5.")
        if values.get('is_published'):
            values['published_date'] = fields.Datetime.now()
        return super(ProductReview, self).write(values)

    # @api.model
    # def set_verified_reviews(self):
    #     review_recs = self.env['product.review'].search([('review_verified','=',False)])
    #     if review_recs:
    #         for each_review in review_recs:
    #             if each_review.customer_id and each_review.customer_id.sale_order_ids:
    #                 update_val = False
    #                 for each_sale_order in each_review.customer_id.sale_order_ids:
    #                     sale_order_recs = each_review.customer_id.sale_order_ids.search([
    #                         ('state','not in',['cancel', 'draft']),
    #                         ('order_line.product_id.product_tmpl_id','=',each_review.product_tmpl_id.id)
    #                     ])
    #                     if sale_order_recs:
    #                         update_val = True
    #                         break
    #                 if update_val:
    #                     each_review.update({'review_verified': True})


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    reviews = fields.One2many('product.review', 'product_tmpl_id', name='reviews', string='Product Reviews')
    avg_rating = fields.Float(compute='_default_rating_average', name='avgRating', string="Product's Average Rating")

    @api.multi
    def _default_rating_average(self):
        total_rating = rating_average = 0.0
        for each_rec in self:
            if each_rec.reviews:
                total_rating += sum(float(each_rev_rec.rev_rating) for each_rev_rec in each_rec.reviews)
                rating_average = total_rating / len(each_rec.reviews)
            each_rec.avg_rating = rating_average

    def get_published_review(self, product_id):
        rv_recs = None
        if product_id:
            review = self.get_featured_review(product_id=product_id)
            if review:
                rv_recs = self.env["product.review"].search([('product_tmpl_id','=',product_id),('is_published','=',True),('id','not in',[review.id])])
            else:
                rv_recs = self.env["product.review"].search([('product_tmpl_id','=',product_id),('is_published','=',True)])
        return rv_recs

    def get_featured_review(self, product_id):
        rv_recs = None
        tag_list = self.env.ref('product_review_management.product_tag_featured').id
        if product_id and tag_list:
            rv_recs = self.env["product.review"].search([('product_tmpl_id','=',product_id),('is_published','=',True),('category_id', 'in', [tag_list])], limit=1, order='rev_rating desc')
        return rv_recs

    def get_published_review_average(self, product_id):
        total_rating_sum = 0.0
        if product_id:
            prod_review_rec = self.env["product.review"].search([('product_tmpl_id','=',product_id),('is_published','=',True)])
            if prod_review_rec:
                total_rating_sum += sum(float(each_rec.rev_rating) for each_rec in prod_review_rec)
                return round((total_rating_sum / len(prod_review_rec)), 1)
        return total_rating_sum


class Website(models.Model):
    _inherit = 'website'

    direct_review_publishing_option = fields.Boolean(name='directReviewPublishingOption', string="Auto Review Publish", help="Do you want to publish review automatically on website?")


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']
    
    direct_review_publishing_option = fields.Boolean(name='directReviewPublishingOption', string="Auto Review Publishing Option", related="website_id.direct_review_publishing_option", help="Do you want to publish review automatically on website?")

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.default'].sudo().set('website', 'direct_review_publishing_option', self.direct_review_publishing_option or False)
        return True

    @api.model
    def get_values(self, fields=None):
        res = super(ResConfigSettings, self).get_values()
        direct_review_publishing_option = self.env['ir.default'].sudo().get('website', 'direct_review_publishing_option')
        res.update({'direct_review_publishing_option': direct_review_publishing_option})
        return res
