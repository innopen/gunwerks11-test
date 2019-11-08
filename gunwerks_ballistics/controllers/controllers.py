# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class GunwerksBallistics(http.Controller):
    @http.route('/gunwerks_ballistics', type='http', auth='public', website=True)
    def index(self, **kw):
        values = {}
        ws_recs = request.env['ballistic.workspace'].sudo().search([])
        values.update({
            'workspaces': ws_recs
        })
        return request.render('gunwerks_ballistics.gw_page', values)

    @http.route('/get_ws_profiles', type='json', auth='public', website=True)
    def get_ws_profiles(self, **kw):
        values = {}
        if kw.get('workspace_id', False):
            ws_rec = request.env['ballistic.workspace'].sudo().browse([int(kw.get('workspace_id'))])
            if ws_rec:
                profiles = []
                if ws_rec.workset_1_profile_id:
                    profiles.append({
                        'id': ws_rec.workset_1_profile_id.id,
                        'name': ws_rec.workset_1_profile_id.name,
                        'bl_data': request.env.ref('gunwerks_ballistics.profile_ballistic_table').render({'profile_id': ws_rec.workset_1_profile_id}),
                        'p_env': ws_rec.workset_1_environment_id.id or ''
                    })
                if ws_rec.workset_2_profile_id:
                    profiles.append({
                        'id': ws_rec.workset_2_profile_id.id,
                        'name': ws_rec.workset_2_profile_id.name,
                        'bl_data': request.env.ref('gunwerks_ballistics.profile_ballistic_table').render({'profile_id': ws_rec.workset_2_profile_id}),
                        'p_env': ws_rec.workset_2_environment_id.id or ''
                    })
                if ws_rec.workset_3_profile_id:
                    profiles.append({
                        'id': ws_rec.workset_3_profile_id.id,
                        'name': ws_rec.workset_3_profile_id.name,
                        'bl_data': request.env.ref('gunwerks_ballistics.profile_ballistic_table').render({'profile_id': ws_rec.workset_3_profile_id}),
                        'p_env': ws_rec.workset_3_environment_id.id or ''
                    })
            values.update({'profiles': profiles})
        return values

    @http.route('/get_profile_info', type='json', auth='public', website=True)
    def get_profile_info(self, **kw):
        ret = {}
        if kw.get('profile_id', False):
            pf_rec = request.env['ballistic.profiles'].browse([int(kw.get('profile_id'))])
            if pf_rec:
                # import pdb; pdb.set_trace()
                ret.update({
                    'pf': {
                        'id': pf_rec.id,
                        'input_units' : pf_rec.input_units,
                        'bullet_diameter': pf_rec.bullet_caliber_id.caliber,
                        'zero_angle_active' : int(pf_rec.zero_angle_active),
                        'zero_range' : pf_rec.zero_range,
                        'zero_angle' : pf_rec.zero_angle,
                        'scope_height': pf_rec.sight_height,
                        'twist_rate': pf_rec.twist,
                        'twist_dir' : dict(pf_rec.fields_get()['twist_dir']['selection']).get(pf_rec.twist_dir),
                        'muzzle_vel' : pf_rec.adj_muzzle_velocity,
                        'bullet_weight' : pf_rec.bullet_weight,
                        'bullet_length' : pf_rec.bullet_length,
                        'drag_function' : dict(pf_rec.fields_get()['drag_function']['selection']).get(pf_rec.drag_function),
                        'bc' : pf_rec.bc,
                        # '' : pf_rec.,
                        # '' : pf_rec.,
                        # '' : pf_rec.,
                        # '' : pf_rec.,
                        # '' : pf_rec.,
                        'bl_grid' : request.env.ref('gunwerks_ballistics.profile_ballistic_table').render({'profile_id': pf_rec}),
                    }
                })
                if kw.get('env_id', False):
                    env_rec = request.env['ballistic.environment'].browse([int(kw.get('env_id'))])
                    if env_rec:
                        ret.update({
                            'env': {
                                'da_active': env_rec.da_active,
                                'density_altitude' : env_rec.density_altitude,
                                'elevation' : env_rec.elevation,
                                'temperature' : env_rec.temp,
                                'pressure' : env_rec.pressure,
                                'humidity' : env_rec.humidity,
                                # 'shot_direction': env_rec.shot_direction,
                                # 'shot_angle': env_rec.shot_angle,
                                # 'shot_cant': env_rec.shot_cant,
                                'latitude': env_rec.latitude,
                                'base_wind': env_rec.base_wind_speed,
                                # 'base_wind_dir': env_rec.base_wind_dir
                            }
                        })
        return ret

