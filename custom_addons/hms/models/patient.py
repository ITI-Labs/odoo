from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date                     
from dateutil.relativedelta import relativedelta  
import re                                   

class Patient(models.Model):
    _name = 'hms.patient'           
    _description = 'HMS Patient'    
    
    first_name = fields.Char(string='First Name', required=True)
    last_name  = fields.Char(string='Last Name',  required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    email = fields.Char(string='Email')
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
    ], string='Blood Type')
    image = fields.Image(string='Patient Image')
    department_id = fields.Many2one('hms.department', string='Department', domain=[('is_opened', '=', True)])
    department_capacity = fields.Integer(related='department_id.capacity', string='Department Capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History', readonly=True)
    
    _sql_constraints = [
        ('uniq_email', 'unique(email)', 'A patient with this email address already exists!')
    ]
    
    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = relativedelta(date.today(), record.birth_date).years
            else:
                record.age = 0

    @api.constrains('email')
    def _check_valid_email(self):
        for record in self:
            if record.email:
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, record.email):
                    raise ValidationError("Please provide a valid email format (e.g., patient@example.com)!")

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Patient, self).create(vals_list)
        for record in records:
            record._create_log(f"Record created. State set to {record.state.capitalize()}")
        return records

    def write(self, vals):
        if 'state' in vals:
            old_state = self.state
            new_state = vals['state']
            if old_state != new_state:
                self._create_log(f"State changed to {new_state.capitalize()}")
        return super(Patient, self).write(vals)

    def _create_log(self, description):
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': description,
        })

    @api.constrains('pcr', 'cr_ratio')
    def _check_pcr_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio field is mandatory when PCR is checked!")

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "Age Notice",
                    'message': "The PCR field has been automatically checked because the patient's age is under 30.",
                    'type': 'notification'
                }
            }

class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'HMS Patient Log'
    _order = 'create_date desc'

    patient_id = fields.Many2one('hms.patient', string='Patient', ondelete='cascade', required=True)
    create_uid = fields.Many2one('res.users', string='Created By', readonly=True)
    create_date = fields.Datetime(string='Date', readonly=True)
    description = fields.Text(string='Description', required=True)