# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    crm_product_ids = fields.One2many(
        'crm.lead', 'product_lead_id', translate=True)
    long_description  = fields.Html(string='Long Description', translate=True)
    short_description = fields.Html(string='Short Description', translate=True)
    special_feature = fields.Html(string='Special Features', translate=True)
    is_gunwerks_template = fields.Boolean(string='Use Gunwerks Template?')
    filter_line_ids = fields.One2many('product.filter.lines', 'product_tmpl_id', 'Product Filters')

    def fill_product_filters(self):
       old_attribute = []
       values = []
       for var in self:
            if var.public_categ_ids:
                for v in var.filter_line_ids:
                    old_attribute.append(v.filter_id.id)
                for category in var.public_categ_ids:
                    for filter_id in category.filter_ids:
                        values.append(filter_id.id)
                        if filter_id.id not in old_attribute:
                            self.env['product.filter.lines'].create({'product_tmpl_id' :var.id,'filter_id' : filter_id.id})
                for i in range(len(old_attribute)):
                    if(old_attribute[i] not in values):
                        search_record = self.env['product.filter.lines'].search(['&',('product_tmpl_id','=',var.id),('filter_id','=', old_attribute[i])])
                        if search_record:
                            search_record.unlink()
            else:
                var.filter_line_ids and var.filter_line_ids.unlink()


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    image = fields.Binary(attachment=True,
        help="This field holds the image used as image for the attribute, limited to 1024x1024px.")
    image_medium = fields.Binary(string="Medium-sized image", attachment=True,
        help="Medium-sized image of the attribute. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved. "
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary(string="Small-sized image", attachment=True,
        help="Small-sized image of the attribute. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    tooltip_notes = fields.Html(string='Tooltip Notes', translate=True)


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    image = fields.Binary(attachment=True,
        help="This field holds the image used as image for the attribute value, limited to 1024x1024px.")
    tooltip_notes = fields.Html(string='Tooltip Notes', translate=True)


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    header_image = fields.Binary(string="Header Image", attachment=True)


class ProductFilters(models.Model):
    _name = "product.filter"
    _description = "Product Filter"
    _order = 'sequence, name'

    name = fields.Char('Name', required=True, translate=True)
    value_ids = fields.One2many('product.filter.value', 'filter_id', 'Values', copy=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")


class ProductFilterValue(models.Model):
    _name = "product.filter.value"
    _order = 'sequence, filter_id, id'

    name = fields.Char('Value', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    filter_id = fields.Many2one('product.filter', 'Filter', ondelete='cascade', required=True)

    _sql_constraints = [
        ('value_company_uniq', 'unique (name,filter_id)', 'This filter value already exists !')
    ]


class ProductFilterLine(models.Model):
    _name = "product.filter.lines"
    _rec_name = 'filter_id'

    product_tmpl_id = fields.Many2one('product.template', 'Product Template', ondelete='cascade', required=True)
    filter_id = fields.Many2one('product.filter', 'Filter', ondelete='restrict', required=True)
    value_ids = fields.Many2many('product.filter.value', string='Filter Values')


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    filter_ids = fields.Many2many('product.filter', string='Filters')
    
