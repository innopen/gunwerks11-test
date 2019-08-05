# -*- coding: utf-8 -*-

from odoo import models, tools, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class EventCategory(models.Model):
    _name = 'event.review.category'
    _description = 'Event Review Tags'

    name = fields.Char(string='Tag Name', required=True, translate=True)
    active = fields.Boolean(default=True, help="The active field allows you to hide the category without removing it.")

class EventReview(models.Model):
    _name = "event.review"
    _rec_name = 'customer_name'
    _order = "is_published desc, crt_date desc"

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
        return self.env['event.review.category'].browse(self._context.get('category_id'))

    name = fields.Char(name='title', string='Title')
    rev_rating = fields.Selection(selection=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], name='revRating', string='Rating', default='1')
    rev_message = fields.Text(name='revMessage', string='Review')
    customer_id = fields.Many2one("res.partner", name='customerId', string="Customer")
    customer_name = fields.Char(name='customerName', string='Customer Name', default=_default_customer)
    crt_date = fields.Datetime(name='crtDate', string='Review Create Date')
    is_published = fields.Boolean(name='isPublished', string='Publish on the website', copy=False)
    published_date = fields.Datetime(name='publishedDate', string='Published Date', default='')
    event_id = fields.Many2one('event.event', name='eventId', string='Event')
    event_category_id = fields.Many2one('event.type', string='Event Category', store=True, related='event_id.event_type_id', readonly=True)
    category_id = fields.Many2many('event.review.category', column1='review_id',
                                    column2='category_id', string='Tags', default=_default_category)

    @api.model
    def create(self, values):
        if 'rev_rating' in values and values['rev_rating']:
            if int(values['rev_rating']) < 1 or int(values['rev_rating']) > 5:
                raise UserError("The Review's rating should be a number between 1 and 5.")
        res = super(EventReview, self).create(values)
        return res

    @api.one
    def write(self, values):
        if values.get('rev_rating'):
            if int(values['rev_rating']) < 1 or int(values['rev_rating']) > 5:
                raise UserError("The Review's rating should be a number between 1 and 5.")
        if values.get('is_published'):
            values['published_date'] = fields.Datetime.now()
        return super(EventReview, self).write(values)


class Event(models.Model):
    _inherit = 'event.event'

    reviews = fields.One2many('event.review', 'event_id', name='reviews', string='Event Reviews')
    avg_rating = fields.Float(compute='_default_rating_average', name='avgRating', string="Event's Average Rating")

    @api.multi
    def _default_rating_average(self):
        total_rating = rating_average = 0.0
        for each_rec in self:
            if each_rec.reviews:
                total_rating += sum(float(each_rev_rec.rev_rating) for each_rev_rec in each_rec.reviews)
                rating_average = total_rating / len(each_rec.reviews)
            each_rec.avg_rating = rating_average

    def get_published_review(self, event_id, event_type_id):
        rec_count = 4
        rv_recs = None
        if event_id:
            review = self.get_featured_review(event_id=event_id, event_type_id=event_type_id)
            if review:
                rv_recs = self.env["event.review"].search([('event_id','=',event_id),('is_published','=',True),('id','not in',[review.id])])
                if len(rv_recs) <= rec_count and event_type_id:
                    rv_recs = self.env["event.review"].search(['&','&',('is_published','=',True),('id','not in',[review.id]),'|',('event_id','=',event_id), ('event_category_id','=',event_type_id)])
            else:
                rv_recs = self.env["event.review"].search([('event_id','=',event_id),('is_published','=',True)])
                if len(rv_recs) <= rec_count and event_type_id:
                    rv_recs = self.env["event.review"].search(['&', ('is_published','=',True), '|', ('event_id','=',event_id), ('event_category_id','=',event_type_id)])
        return rv_recs

    def get_featured_review(self, event_id, event_type_id):
        rv_recs = None
        tag_list = self.env.ref('event_review_management.event_tag_featured').id
        if event_id and tag_list:
            rv_recs = self.env["event.review"].search([('event_id','=',event_id),('is_published','=',True),('category_id', 'in', [tag_list])], limit=1, order='rev_rating desc')
        if not rv_recs and tag_list and event_type_id:
            rv_recs = self.env["event.review"].search([('event_category_id','=',event_type_id),('is_published','=',True),('category_id', 'in', [tag_list])], limit=1, order='rev_rating desc')
        return rv_recs

    def get_published_review_average(self, event_id, event_type_id):
        total_rating_sum = 0.0
        rec_count = 4
        if event_id:
            event_review_rec = self.env["event.review"].search([('event_id','=',event_id),('is_published','=',True)])
            if len(event_review_rec) <= rec_count and event_type_id:
                event_review_rec = self.env["event.review"].search(['&', ('is_published','=',True), '|', ('event_id','=',event_id), ('event_category_id','=',event_type_id)])
                if event_review_rec:
                    total_rating_sum += sum(float(each_rec.rev_rating) for each_rec in event_review_rec)
                    return round((total_rating_sum / len(event_review_rec)), 1)
            elif event_review_rec:
                total_rating_sum += sum(float(each_rec.rev_rating) for each_rec in event_review_rec)
                return round((total_rating_sum / len(event_review_rec)), 1)
        return total_rating_sum
