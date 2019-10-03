# -*- coding: utf-8 -*-

from odoo import models, fields, api

#All the fields required to calculate a Ballistic solution
class BallisticProfiles(models.Model):
    _name = 'ballistic.profiles'

#General Info
    name = fields.Char('Profile Name')
    res_partner_id = fields.Many2one('res.partner', domain="[('customer', '=', True)]")
    input_units = fields.Selection([('us','US'),('si','SI')], string="Input Units")

#Weapon Details
    bullet_caliber_id = fields.Many2one('bullet.caliber')
    bullet_caliber = fields.Float('Bullet Caliber') #this will be used to store the caliber form bullet.caliber or a custom entry if "custom" is selected
    twist = fields.Float('Twist Rate 1:XX')
    twist_dir = fields.Selection([('right','Right'),('left','Left')], string='Twist Direction')
    sight_height = fields.Float('Sight Height')    
    zero_range = fields.Float()
    zero_elevation_offset = fields.Float()
    zero_angle_active = fields.Boolean('Use Zero Angle')
    zero_angle = fields.Float() #Need to be computed using zero_angle_calc if customer doesn't have it.
    turret_adj_active = fields.Boolean('Adjust Turret Click Values')
    elevation_adj_factor = fields.Float('Elevation Correction')
    wind_adj_factor = fields.Float('Windage Correction')
    
    #Turret Options
    custom_turret_active = fields.Boolean('Use Custom Turret')
    turret_altitude = fields.Integer()
    turret_mv = fields.Integer()
    bdc_units = fields.Selection(selection=[('yards','Yards'),('meters','Meters')], string='BDC Units')
    load_desc = fields.Text('Load Description')


#Bullet Details
    bullet_custom = fields.Boolean('Use Custom Bullet Profile')
    bullet_mfg_id = fields.Many2one('bullet.mfg', string='Bullet MFG')
    bullet_model_id = fields.Many2one('bullet.model')
    drag_function = fields.Selection([('g1','G1'),('g7','G7'),('doppler','Doppler')])
    doppler_length = fields.Integer()# think this should just be a calculated field from the doppler file json string - don't even know if we need this field
    doppler_file = fields.Char() #Store as a JSON String?
    bc = fields.Float('BC')
    bullet_lenght = fields.Float()
    bullet_weight = fields.Float()

#MV Details
    measured_muzzle_velocity = fields.Integer()
    muzzle_chrono_distance = fields.Float()
    adj_muzzle_velocity = fields.Integer('Actual Muzzle Velocity') #Use a calulation to determan actual mv from inputs above.

    powder_factor_active = fields.Boolean('Use Powder Factor Compensation')
    base_powder_temp = fields.Float()
    powder_factor = fields.Float()

    # #Muzzle Velocity Correction Inputs
    # def mv_correction(self):

    # #Zero Angle Settings
    # def zero_angle_calc(self):
    #     Zero Range - Pull from Odoo field
    #     Zero Elevation Offset - Pull from Odoo field
    #     Zero Windage Offset
    #     Zero Temperature
    #     Zero Pressure
    #     Zero Humidity
    #     Zero Shooting Angle
    #     Wind Speed 
    #     Wind Direction   
    #     Barrel Twist - Pull from Odoo Fields

class BallisticEnviroment(models.Model):
    _name = 'ballistic.enviroment'

    name = fields.Char()
    res_partner_id = fields.Many2one('res.partner', domain="[('customer', '=', True)]")

    da_active = fields.Boolean('Use Density Altitude')
    density_altitude = fields.Integer()
    
    pressure = fields.Float('Station Pressure')
    elevation = fields.Integer()
    temp = fields.Integer()
    humidity = fields.Integer()    
    latitude = fields.Float()
    base_wind_speed = fields.Float()


class BulletCaliber(models.Model):
    _name = 'bullet.caliber'

    name = fields.Char()
    caliber = fields.Float('Caliber in Inches', digits=(4,3))

class BulletMaker(models.Model):
    _name = 'bullet.mfg'

    name = fields.Char()
    bullet_model_ids = fields.Many2many('bullet.model')


class BulletModel(models.Model):
    _name = 'bullet.model'

    name = fields.Char()
    bullet_caliber_id = fields.Many2one('bullet.caliber')
    bullet_mfg_id = fields.Many2one('bullet.mfg')
    g1_available = fields.Boolean()
    g1 = fields.Float()
    g7_available = fields.Boolean()
    g7 = fields.Float()
    doppler_available = fields.Boolean()
    doppler_file = fields.Char()


class PartnerBallistics(models.Model):
    _inherit = 'res.partner'

    ballistic_profiles_ids = fields.Many2many('ballistic.profiles')