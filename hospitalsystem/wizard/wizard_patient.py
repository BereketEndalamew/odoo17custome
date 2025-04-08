from odoo import models, fields
from datetime import datetime

class HospitalWizard(models.TransientModel):
    _name = 'hospital.wizard'
    _description = 'Hospital Wizard'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    age = fields.Integer(related='patient_id.age', string='Age', readonly=True)
    gender = fields.Selection(related='patient_id.gender', string='Gender', readonly=True)
    phone = fields.Char(related='patient_id.phone', string='Phone', readonly=True)
    email = fields.Char(related='patient_id.email', string='Email', readonly=True)
    appointement_date = fields.Datetime(string="Appointement Date", required=True)
    notes = fields.Text(string="Notes")
    seen_status = fields.Boolean(string="Seen")

    def wizardview(self):
        vals = {
            'patient_id': self.patient_id.id,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'appointement_date': self.appointement_date,
            # 'notes': self.notes,
            # 'seen_status': self.seen_status,
        }

        # Create a new record in the 'hospital.appointment' model
        self.env['hospital.appointement'].create(vals)

        # Optionally, you may want to close the wizard and return the view
