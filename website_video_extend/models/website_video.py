# -*- coding: utf-8 -*-

import base64
from odoo import models, fields, api
from odoo.http import request
            	

class WebsiteVideo(models.Model):
    _name = 'website.video.content'
    _description = 'Website Video'  

    name = fields.Char(string='Name', translate=True)
    file_name = fields.Char(string='Name of File', translate=False)
    video_cover_image = fields.Binary(string="Video Cover Image")
    video_cover_image_file = fields.Char(string='Name of File', translate=False)
    video_file = fields.Binary(string="Video File",store=True,attachment=True)
    active = fields.Boolean(string="Active")
    
    @api.model    
    def get_file_content(self,content_id=0):
        decode_data =''
        data = self.env['website.video.content'].sudo().search([('id','=',int(content_id))])
        
        if data and data.video_file:
            self.env.cr.execute("select * from ir_attachment where res_id="+ str(data.id)+"and res_model='website.video.content' ")
            attachment = self.env.cr.dictfetchall()
            if attachment:
            	return attachment
    

class Website(models.Model):
    _inherit = 'website'


    @api.model    
    def get_videos(self,content_id=0):
        data = self.env['website.video.content'].sudo().search([('active','=',True)])        
        if data:
            return data
        return False  
