# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TurretLayout(models.Model):
    _name = 'turret.layout'

    name = fields.Char('Turret Layout Name')
    turret_part = fields.Many2one('product.template', string='Turret Part')

    #Laser Offset Details
    laser_offsets_ids = fields.Many2many('laser.offsets')
    turret_laser_id = fields.Many2one(related='laser_offsets_ids.turret_laser_id')

    #Turret Style in TurretExpress
    face_height = fields.Float('Face Height')
    face_diameter = fields.Float('Face Diameter')
    adj_rev = fields.Integer('Adjustment Per Rev')
    cap_innner_dia = fields.Float('Top Cap Inner Diameter')
    cap_outer_dia = fields.Float('Top Cap Outer Diameter')
    adj_dir = fields.Selection(selection=[('cc','Counter-Clockwise'),('cw','Clockwise')], string='Direction of Adjustment')
    angle_units = fields.Selection(selection=[('moa','MOA'),('mrad','MRAD')], string='Angle Units')
    click_units = fields.Selection(selection=[('1','1'),('.5','.5'),('.33','.33'),('.25','.25'),('.125','.125'),('.1','.1'),('.05','.05')], string='Click Units')

    #Turret Layout Detials
    #Top Cap Settings
    top_cap_active = fields.Boolean('Engrave Top Cap')
    top_cap_inner_data = fields.Selection(selection=[('none','NONE'),('click value','Click Value - Direction')], string='Inner Data')
    top_cap_inner_font = fields.Integer('Inner Font Size')
    top_cap_outer_data = fields.Selection(selection=[('none','NONE'),('click value','Click Value - Direction')], string="Outter Data")
    top_cap_outer_font = fields.Integer('Outer Font Size')
    
    #Top Row Settings
    top_row_active = fields.Boolean('Add Top Row')
    top_info_type = fields.Selection(selection=[('bdc','BDC'),('turret data','Turret Data')], string="Info Type")
    top_font_size = fields.Integer('Font Size')
    top_line_width = fields.Float('Line Width')
    top_row_height = fields.Integer('Row Height')
    top_100_line_height = fields.Integer('100 Line Height')
    top_50_line_height = fields.Integer('50 Line Height')
    top_25_line_height = fields.Integer('25 Line Height')

    #Middle Row Settings
    middle_row_active = fields.Boolean('Add Middle Row')
    middle_info_type = fields.Selection(selection=[('bdc','BDC'),('turret data','Turret Data')], string="Info Type")
    middle_font_size = fields.Integer('Font Szie')
    middle_line_width = fields.Float('Line Width')
    middle_row_height = fields.Integer('Row Height')
    middle_100_line_height = fields.Integer('100 Line Height')
    middle_50_line_height = fields.Integer('50 Line Height')
    middle_25_line_height = fields.Integer('25 Line Height')

    #Bottom Row Settings
    bottom_row_active = fields.Boolean('Add Bottom Row')
    bottom_info_type = fields.Selection(selection=[('bdc','BDC'),('turret data','Turret Data')], string="Info Type")
    bottom_font_size = fields.Integer('Font Szie')
    bottom_line_width = fields.Float('Line Width')
    bottom_row_height = fields.Integer('Row Height')
    bottom_100_line_height = fields.Integer('100 Line Height')
    bottom_50_line_height = fields.Integer('50 Line Height')
    bottom_25_line_height = fields.Integer('25 Line Height')

class TurretJob(models.Model):
    _name = 'turret.job'

    turret_profile_id = fields.Many2one('turret.layout', string='Turret Profile')
    ballistic_profile_id = fields.Many2one('ballistic.profiles', string='Ballistic Profile')
    mrp_production_id = fields.Many2one('mrp.production', string='Manufacturing Order')
    top_turret_laser_id = fields.Many2one('turret.laser', string='Laser For Top Cap')
    face_turret_laser_id = fields.Many2one('turret.laser', string='Laser For Face')


# class TurretData(models.Model):
#     _name = 'turret.data'


class TurretLaser(models.Model):
    _name = 'turret.laser'

    name = fields.Char('Laser Name')
    x_axis_len = fields.Float('X Axis Length')
    y_axis_len = fields.Float('Y Axis Length')

class LaserOffsets(models.Model):
    _name = 'laser.offsets'

    # @api.one
    # @api.depends('turret_laser_id','turret_layout_id')
    # def _compute_name(self):
    #     self.name = self.turret_laser_id.name + " - " + self.turret_layout_id.name

    name = fields.Char() #(compute=_compute_name)
    turret_laser_id = fields.Many2one('turret.laser')
    turret_layout_id = fields.Many2one('turret.layout')
    face_x_shift = fields.Float('X Shift for Face Tooling')
    face_y_shift = fields.Float('Y Shift for Face Tooling')
    cap_x_shift = fields.Float('X Shift for Cap Tooling')
    cap_y_shift = fields.Float('Y Shift for Face Tooling')

