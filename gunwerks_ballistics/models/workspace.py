# -*- coding: utf-8 -*-

from odoo import models, fields, api


#Model to Store a website users workspace and settings
class BallisticWorkspace(models.Model):
    _name = 'ballistic.workspace'

    name = fields.Char('Workspace Name')    
    res_user_id = fields.Many2one('res.users')
    
    min_range = fields.Integer()
    max_range = fields.Integer()
    range_increment = fields.Integer()

    workset_1_profile_id = fields.Many2one('ballistic.profiles')
    workset_1_environment_id = fields.Many2one('ballistic.environment')
    workset_1_data = fields.Text()

    workset_2_profile_id = fields.Many2one('ballistic.profiles')
    workset_2_environment_id = fields.Many2one('ballistic.environment')
    workset_2_data = fields.Text()

    workset_3_profile_id = fields.Many2one('ballistic.profiles')
    workset_3_environment_id = fields.Many2one('ballistic.environment')
    workset_3_data = fields.Text()

    #Settings
    spin_drift_active = fields.Boolean()
    coriolis_active = fields.Boolean()
    air_jump_active = fields.Boolean()
    target_lead_active = fields.Boolean()

    def test(self):
        pass
