from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError


class PersonalInformation(models.Model):
    _name = 'personal.info'
    _description = 'Personal Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit from mail.thread to enable messaging
    _rec_name = 'employe_id'
    employe_id = fields.Many2one('hr.employee',string='Employe', required=True)
    email = fields.Char(related='employe_id.work_email',string='Email Address', required=True)
    phone = fields.Char(string='Phone Number', required=True)


    def open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Registration Page',
            'view_mode': 'form',
            'res_model': 'travel.wizard',
             'context': {'default_employe_id': self.employe_id.id},  # Prefill patient_id
            'target': 'new',
        }
