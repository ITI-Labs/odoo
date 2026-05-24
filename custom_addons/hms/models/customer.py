from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')

    @api.constrains('email')
    def _check_patient_email_conflict(self):
        for record in self:
            if record.email:
                matched_patient = self.env['hms.patient'].search([('email', '=', record.email)], limit=1)
                if matched_patient:
                    raise ValidationError(f"The email '{record.email}' belongs to an existing patient profile.")

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise ValidationError("You cannot delete a customer linked to a patient profile.")
        return super(ResPartner, self).unlink()