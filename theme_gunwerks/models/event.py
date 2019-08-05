# -*- coding: utf-8 -*-


import base64
from odoo import api, fields, models, _
from odoo import modules, tools
from datetime import datetime
from odoo.modules.module import get_module_resource
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import ValidationError


class EventType(models.Model):
    _inherit = ['event.type']

    @api.model
    def create(self, vals):
        if not vals.get('event_icon'):
            img_path = get_module_resource(
                'theme_gunwerks', 'static/src/img', 'default-180-180.jpg')
            if img_path:
                with open(img_path, 'rb') as f:
                    image = f.read()
            vals['event_icon'] = tools.image_resize_image_big(
                base64.b64encode(image))
        return super(EventType, self).create(vals)

    event_icon = fields.Binary(
        help='Display a Event Category Icon')


class MainEvent(models.Model):
    _inherit = ['event.event']

    def _get_default_question(self):
        result = """
                <div class="container">
                    <div class="row">
                        <div class="col-md-6 col-md-offset-3">
                            <h5>QUESTIONS?</h5>
                            <p>Contact Kari Hinther, <span>Events Manager</span></p>
                            <p>307-296-7297<br/><a href="mailto:Kari@gunwerks.com">Kari@gunwerks.com</a></p>
                        </div>
                    </div>
                </div>"""

        return result

    def _get_default_policy(self):
        result = """
                <div class="container">
                    <div class="row">
                        <div class="col-md-6 col-md-offset-3">
                            <h6>CANCELLATION POLICY:</h6>
                            <ul class="list-type-arrow">
                                <li>L1, L2, L3 - $500 deposit due upon order. L4 - $1000 deposit due upon order.</li>
                                <li>Gunwerks LLC. reserves the right to cancel any class that does not meet the 4 person minimum 30 days prior to school date.</li>
                                <li>Upto 45 days prior to the course - deposit is completely refundable.</li>
                                <li>Up to 30 days prior to the course - deposit non-refundable, but can be moved to the another date. (After 30 days prior, deposit not refundable and not movable).</li>
                                <li>15 days prior to the course - payment in full due, no refunds.</li>
                            </ul>
                        </div>
                    </div>
                </div>"""

        return result

    def _get_default_overview(self):
        result = """
                <section class="event-training-overview-snippet">
                    <div class="container">
                        <div class="row">
                            <div class="col-md-12"><h5>TRAINING OVERVIEW</h5></div>
                        </div>
                        <div class="row">
                            <div class="col-md-5 col-md-offset-1">
                                <ul class="list-type-arrow">
                                    <li>Understanding the LRR System</li>
                                    <li>Overview of Main Components of the LRRS</li>
                                    <li>Rifle Scopes - Understanding  MOA and Milliradian, Features, 1st and 2nd Focal Plane, Using Wind Holds and Parallax</li>
                                    <li>Proper Zeroing and setting the Zerostop</li>
                                    <li>Ammunition - Terminal Performance, Low Wind Deflection, Minimize Vertical and bullet Types</li>
                                    <li>Rangefinder - Range Accuracy, Maximum Range, Specification and Function, Target Measurement/ Detection, Measurement Modes, Setting Profiles and Bonus Functions/Devices</li>
                                </ul>
                            </div>
                            <div class="col-md-5">
                                <ul class="list-type-arrow">
                                    <li>Precision Shooting - Bench Techniques, Shooting to Rifles Potential, Parity with Field Shooting, Proper Support, Body Position, Breathing, Trigger Control, Techniques, Free Recoil, The Grip, Anchor Point, Bag Pressure, Two Point Support, Follow Through and Spotting Techniques</li>
                                    <li>Cleaning and Maintenance - Classroom Discussion and Demonstration, Tools and Supplies, Techniques</li>
                                    <li>External Ballistics - Spindrift (SD) and Mitigating SD</li>
                                    <li>Shooting out to 1000 yards Practical exercises</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </section>"""

        return result

    def _get_event_desc(self):
        result = """
                <p style="text-align: center; ">
                    <b><font style="font-size: 24px;">Event Description</font></b>
                </p>"""

        return result

    @api.one
    def mail_attendees(self, template_id, force_send=False, filter_func=lambda self: self.state != 'cancel'):
        final_list = []
        attendee_list = {}
        count = 0

        for attendee in self.registration_ids.filtered(filter_func):
            if not attendee.email in attendee_list.values():
                count = count + 1
                attendee_list[count] = attendee.email
                final_list.append(attendee.id)

        res = super(MainEvent, self).mail_attendees(template_id, force_send=False,
                                                    filter_func=lambda self: self.state != 'cancel' and self.id in final_list)
        return res

    event_desc = fields.Html(string='Event Description',
                             translate=True, default=_get_event_desc)
    event_direction = fields.Html(string='Directions', translate=True)
    event_stay_travel = fields.Html(string='Lodging', translate=True)
    event_travel = fields.Html(string='Travel', translate=True)
    event_arrival = fields.Html(string='Arrival', translate=True)
    event_itr = fields.Html(string='Itinerary', translate=True)
    event_thing = fields.Html(string='What to Bring', translate=True)
    crm_event_ids = fields.One2many('crm.lead', 'event_lead_id')
    image = fields.Binary(string='Image', help='Display a Event Image')
    event_image_ids = fields.One2many(
        'event.image', 'event_id', string='Images')
    location_image_ids = fields.One2many(
        'event.location.image', 'event_id', string='Location Images')
    training_overview = fields.Html(
        string='Training Overview', translate=True, default=_get_default_overview)
    location_description = fields.Text(
        string='Location Description', translate=True)
    faq = fields.Html(string='FAQ', translate=True)
    question = fields.Html(
        string='Question?', translate=True, default=_get_default_question)
    cancellation_policy = fields.Html(
        string='Cancellation Policy', translate=True, default=_get_default_policy)

    @api.model
    def create(self, vals):
        if not vals.get('image'):
            img_path = get_module_resource(
                'theme_gunwerks', 'static/src/img', 'default-600-600.jpg')
            if img_path:
                with open(img_path, 'rb') as f:
                    image = f.read()
            vals['image'] = tools.image_resize_image_big(
                base64.b64encode(image))
        return super(MainEvent, self).create(vals)

    @api.one
    @api.constrains('event_ticket_ids')
    def _check_end_date(self):
        for date in self.event_ticket_ids:
            if date.event_ends < date.event_start:
                raise ValidationError(
                    _('End Date cannot be set before Start Date.'))

    @api.constrains('event_ticket_ids')
    def on_change_date(self):
        min_date = []
        max_date = []
        for i in self.event_ticket_ids:
            min_date.append(i.event_start)
            max_date.append(i.event_ends)
        self.date_begin = min(min_date)
        self.date_end = max(max_date)


class EventImage(models.Model):
    _name = 'event.image'
    _description = 'Event Image'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True, required=True)
    event_id = fields.Many2one('event.event', 'Related Event', copy=True)


class EventLocationImage(models.Model):
    _name = 'event.location.image'
    _description = 'Event Location Image'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True, required=True)
    event_id = fields.Many2one('event.event', 'Related Event', copy=True)


class GunwerksEventTicket(models.Model):
    _inherit = 'event.event.ticket'

    #sales_start = fields.Date(string="Sales Start")
    event_start = fields.Datetime(string="Event Start")
    event_ends = fields.Datetime(string="Event Ends")

    # @api.multi
    # def _compute_is_expired(self):
    #     for record in self:
    #         current_date = fields.Date.context_today(record.with_context({'tz': record.event_id.date_tz}))
    #         if record.deadline and record.sales_start:
    #             record.is_expired = (record.deadline < current_date or current_date < record.sales_start)
    #         elif record.sales_start and not record.deadline:
    #             record.is_expired = current_date < record.sales_start
    #         elif record.deadline and not record.sales_start:
    #             record.is_expired = record.deadline < current_date
    #         else:
    #             record.is_expired = False


class WebsitePage(models.Model):
    _inherit = "website.page"

    crm_page_ids = fields.One2many('crm.lead', 'page_lead_id', translate=True)


class EventLead(models.Model):
    _inherit = ['crm.lead']
    lead_source = fields.Selection(
        [('product', 'Product'), ('event', 'Event'), ('page', 'CMS Page')], translate=True)
    event_lead_id = fields.Many2one(
        'event.event', string='Event', translate=True)
    page_lead_id = fields.Many2one(
        'website.page', string='Page', translate=True)
    product_lead_id = fields.Many2one(
        'product.template', string='Product', translate=True)

    def website_form_input_filter(self, request, values):
        res = super().website_form_input_filter(request, values)
        if request.params.get('event_info'):
            event_name = request.params.get('event_info')
            res['event_lead_id'] = event_name
        elif request.params.get('prod_info'):
            product_name = request.params.get('prod_info')
            res['product_lead_id'] = product_name
        return res

    @api.model
    def create(self, values):
        rec = super(EventLead, self).create(values)
        if rec.event_lead_id:
            rec.lead_source = 'event'
        if rec.product_lead_id:
            rec.lead_source = 'product'
        return rec
