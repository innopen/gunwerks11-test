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
    bullet_length = fields.Float()
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

    def run_ballistic_calc(self):
        self.ensure_one()
        ret = {1025: {'time_of_flight': 1.56, 'drift': 8.186644594921306, 'drop': -387.35636044533385, 'velocity': 1441.9164089778906, 'wind2': 0.0}, 900: {'time_of_flight': 1.311, 'drift': 5.9552616540468915, 'drop': -281.3708758328585, 'velocity': 1573.2722079087102, 'wind2': 0.0}, 775: {'time_of_flight': 1.082, 'drift': 4.1910593318712275, 'drop': -197.39000229580054, 'velocity': 1710.802704476756, 'wind2': 0.0}, 650: {'time_of_flight': 0.872, 'drift': 2.823794508452722, 'drop': -132.01108177947484, 'velocity': 1854.6761708658473, 'wind2': 0.0}, 525: {'time_of_flight': 0.677, 'drift': 1.776908993912122, 'drop': -82.45622492844853, 'velocity': 2004.5493140556646, 'wind2': 0.0}, 400: {'time_of_flight': 0.497, 'drift': 1.0092996281694007, 'drop': -46.44327587100775, 'velocity': 2161.095289488684, 'wind2': 0.0}, 275: {'time_of_flight': 0.33, 'drift': 0.4770549778272776, 'drop': -22.079743157337674, 'velocity': 2324.071835178358, 'wind2': 0.0}, 1300: {'time_of_flight': 2.194, 'drift': 15.280970678946053, 'drop': -720.3317631165701, 'velocity': 1174.334663645854, 'wind2': 0.0}, 150: {'time_of_flight': 0.17400000000000002, 'drift': 0.14787441727716188, 'drop': -7.788502128746634, 'velocity': 2492.111516599738, 'wind2': 0.0}, 1175: {'time_of_flight': 1.889, 'drift': 11.619632827807152, 'drop': -549.5856166719328, 'velocity': 1291.1858154043844, 'wind2': 0.0}, 25: {'time_of_flight': 0.028, 'drift': 0.005223806954460316, 'drop': -2.255608777940788, 'velocity': 2664.8521014072185, 'wind2': 0.0}, 1050: {'time_of_flight': 1.612, 'drift': 8.692925155471997, 'drop': -411.54743816834616, 'velocity': 1416.2479716064279, 'wind2': 0.0}, 925: {'time_of_flight': 1.359, 'drift': 6.360328220376879, 'drop': -300.68598511739805, 'velocity': 1546.526824198494, 'wind2': 0.0}, 800: {'time_of_flight': 1.1260000000000001, 'drift': 4.5082000191866785, 'drop': -212.5990660801315, 'velocity': 1682.7920602654608, 'wind2': 0.0}, 675: {'time_of_flight': 0.912, 'drift': 3.065338755007115, 'drop': -143.73992868281005, 'velocity': 1825.4081107910936, 'wind2': 0.0}, 550: {'time_of_flight': 0.715, 'drift': 1.963667617788353, 'drop': -91.2170344339529, 'velocity': 1974.0717752658888, 'wind2': 0.0}, 425: {'time_of_flight': 0.532, 'drift': 1.14315786581181, 'drop': -52.65825870652309, 'velocity': 2129.2434277702273, 'wind2': 0.0}, 300: {'time_of_flight': 0.362, 'drift': 0.5650990874144406, 'drop': -26.10030948740321, 'velocity': 2291.0347912281977, 'wind2': 0.0}, 1325: {'time_of_flight': 2.259, 'drift': 16.11961349796155, 'drop': -758.9840934440714, 'velocity': 1152.8186734001938, 'wind2': 0.0}, 175: {'time_of_flight': 0.20400000000000001, 'drift': 0.1978386447225413, 'drop': -9.907423586075463, 'velocity': 2458.146242315476, 'wind2': 0.0}, 1200: {'time_of_flight': 1.948, 'drift': 12.292372292503165, 'drop': -580.9185790135697, 'velocity': 1266.9979291895663, 'wind2': 0.0}, 50: {'time_of_flight': 0.057, 'drift': 0.01918398860347089, 'drop': -2.7170313240162294, 'velocity': 2629.896959336184, 'wind2': 0.0}, 1075: {'time_of_flight': 1.665, 'drift': 9.223080030774994, 'drop': -436.82185046982266, 'velocity': 1390.7785325276109, 'wind2': 0.0}, 950: {'time_of_flight': 1.408, 'drift': 6.786264461905956, 'drop': -320.909389581111, 'velocity': 1520.0443284577807, 'wind2': 0.0}, 825: {'time_of_flight': 1.171, 'drift': 4.843363224401507, 'drop': -228.57518318541634, 'velocity': 1655.0403753628686, 'wind2': 0.0}, 700: {'time_of_flight': 0.9540000000000001, 'drift': 3.328598764028524, 'drop': -156.12055103706962, 'velocity': 1796.3817084518344, 'wind2': 0.0}, 575: {'time_of_flight': 0.753, 'drift': 2.158851294156759, 'drop': -100.53513331630448, 'velocity': 1943.8757808776131, 'wind2': 0.0}, 450: {'time_of_flight': 0.5670000000000001, 'drift': 1.2845319759129077, 'drop': -59.352206605167275, 'velocity': 2097.659164087196, 'wind2': 0.0}, 325: {'time_of_flight': 0.395, 'drift': 0.6629192141732331, 'drop': -30.53459379425843, 'velocity': 2258.203707000085, 'wind2': 0.0}, 1350: {'time_of_flight': 2.324, 'drift': 16.978527729840103, 'drop': -799.2731958133843, 'velocity': 1132.2774910836395, 'wind2': 0.0}, 200: {'time_of_flight': 0.23500000000000001, 'drift': 0.25629616619005235, 'drop': -12.385744997245753, 'velocity': 2424.352498155206, 'wind2': 0.0}, 1225: {'time_of_flight': 2.008, 'drift': 12.994079166553442, 'drop': -613.6058696417562, 'velocity': 1243.115558512372, 'wind2': 0.0}, 75: {'time_of_flight': 0.085, 'drift': 0.0398588308705758, 'drop': -3.492364701148326, 'velocity': 2595.140469362702, 'wind2': 0.0}, 1100: {'time_of_flight': 1.72, 'drift': 9.788248346915974, 'drop': -463.2198869966658, 'velocity': 1365.5161580638905, 'wind2': 0.0}, 975: {'time_of_flight': 1.457, 'drift': 7.224684754407194, 'drop': -342.0731047848436, 'velocity': 1493.816814638281, 'wind2': 0.0}, 850: {'time_of_flight': 1.217, 'drift': 5.197202994846154, 'drop': -245.34429824473563, 'velocity': 1627.5337649174523, 'wind2': 0.0}, 725: {'time_of_flight': 0.996, 'drift': 3.601658329503796, 'drop': -169.1742188383015, 'velocity': 1767.6021044636857, 'wind2': 0.0}, 600: {'time_of_flight': 0.792, 'drift': 2.3678544555897356, 'drop': -110.42796235613571, 'velocity': 1913.9156931552232, 'wind2': 0.0}, 475: {'time_of_flight': 0.603, 'drift': 1.4377010936094636, 'drop': -66.53971610176735, 'velocity': 2066.346343482167, 'wind2': 0.0}, 350: {'time_of_flight': 0.429, 'drift': 0.7710539504216326, 'drop': -35.39469460317583, 'velocity': 2225.585662316745, 'wind2': 0.0}, 1375: {'time_of_flight': 2.391, 'drift': 17.88498359658471, 'drop': -841.2591854823588, 'velocity': 1112.8976539262787, 'wind2': 0.0}, 225: {'time_of_flight': 0.266, 'drift': 0.32152986406758205, 'drop': -15.233529654945125, 'velocity': 2390.73750073669, 'wind2': 0.0}, 1250: {'time_of_flight': 2.069, 'drift': 13.725545689124408, 'drop': -647.7002147133969, 'velocity': 1219.564367384831, 'wind2': 0.0}, 100: {'time_of_flight': 0.115, 'drift': 0.06930506412953384, 'drop': -4.590180260549338, 'velocity': 2560.588495454991, 'wind2': 0.0}, 1125: {'time_of_flight': 1.7750000000000001, 'drift': 10.36861898792975, 'drop': -490.7834404997534, 'velocity': 1340.4685699739748, 'wind2': 0.0}, 1000: {'time_of_flight': 1.508, 'drift': 7.694180616080861, 'drop': -364.21048297321624, 'velocity': 1467.7755600619007, 'wind2': 0.0}, 875: {'time_of_flight': 1.2630000000000001, 'drift': 5.562321065654531, 'drop': -262.9334545070366, 'velocity': 1600.2760756040623, 'wind2': 0.0}, 750: {'time_of_flight': 1.039, 'drift': 3.8912969522584766, 'drop': -182.92299897870825, 'velocity': 1739.0741947071006, 'wind2': 0.0}, 625: {'time_of_flight': 0.8310000000000001, 'drift': 2.585578902474793, 'drop': -120.91363065570462, 'velocity': 1884.180552542551, 'wind2': 0.0}, 500: {'time_of_flight': 0.64, 'drift': 1.6032353283765655, 'drop': -74.23586929092826, 'velocity': 2035.3085940952287, 'wind2': 0.0}, 375: {'time_of_flight': 0.463, 'drift': 0.8865457158091519, 'drop': -40.69323005731368, 'velocity': 2193.2107446973846, 'wind2': 0.0}, 1400: {'time_of_flight': 2.459, 'drift': 18.82677920980592, 'drop': -885.0015630117044, 'velocity': 1095.6679128232245, 'wind2': 0.0}, 250: {'time_of_flight': 0.298, 'drift': 0.39582542353332073, 'drop': -18.461229740161503, 'velocity': 2357.3083079763665, 'wind2': 0.0}, 1275: {'time_of_flight': 2.1310000000000002, 'drift': 14.487572918319932, 'drop': -683.2565928942408, 'velocity': 1196.6187361927016, 'wind2': 0.0}, 125: {'time_of_flight': 0.14400000000000002, 'drift': 0.10459026958540055, 'drop': -6.01922632617406, 'velocity': 2526.2466719039317, 'wind2': 0.0}, 1150: {'time_of_flight': 1.832, 'drift': 10.986048975249705, 'drop': -519.5566718805293, 'velocity': 1315.6769173544508, 'wind2': 0.0}}
        return ret

    def ballistic_heads(self):
        ret = [
            {'col_key': 'range', 'name': 'Range', 'mu': 'yds'},
            {'col_key': 'drop', 'name': 'Drop', 'mu': 'moa'},
            {'col_key': 'wind', 'name': 'Wind', 'mu': 'moa'},
            {'col_key': 'drop2', 'name': 'Drop', 'mu': 'in'},
            {'col_key': 'wind2', 'name': 'Wind', 'mu': 'in'},
            {'col_key': 'velocity', 'name': 'Velocity', 'mu': 'fps'},
            {'col_key': 'drift', 'name': 'Energy', 'mu': 'ft-lbs'},
            {'col_key': 'time_of_flight', 'name': 'TOF', 'mu': 'sec'},
        ]
        return ret


class BallisticEnviroment(models.Model):
    _name = 'ballistic.environment'

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


