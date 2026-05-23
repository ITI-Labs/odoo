from odoo import models, fields

class Patient(models.Model):
    _name = 'hms.patient'           
    _description = 'HMS Patient'    
    first_name = fields.Char(string='First Name', required=True)
    last_name  = fields.Char(string='Last Name',  required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age')
    address = fields.Text(string='Address')
    history = fields.Html(string='Medical History')
    cr_ratio = fields.Float(string='CR Ratio')
    pcr = fields.Boolean(string='PCR')
    blood_type = fields.Selection(selection=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ],string='Blood Type')
    image = fields.Image(string='Patient Image')