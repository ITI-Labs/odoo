from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'HMS Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Image(string='Image')