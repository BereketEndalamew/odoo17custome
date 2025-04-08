import logging
import requests
from odoo import api, models, fields
from datetime import date, timedelta, datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital System'

    name = fields.Char(string='Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email')
    appointement_count = fields.Integer(
        string='Appointement Count',
        compute='_compute_appointement_count',
        store=True
    )
    country_id = fields.Many2one('res.country', string="Country", default=lambda self: self.env.ref('base.et').id)
    state_id = fields.Many2one('res.country.state', string="State/Region", domain="[('country_id', '=', country_id)]")

    # city_id = fields.Many2one('res.city', string="City", domain="[('state_id', '=', state_id)]")
    # woreda_id = fields.Many2one('res.woreda', string="Woreda", domain="[('city_id', '=', city_id)]")
    # kebele_id = fields.Many2one('res.kebele', string="Kebele", domain="[('woreda_id', '=', woreda_id)]")

    def viewdata(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'View Appointements',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointement',
            'domain': [('patient_id', '=', self.id)],
            'target': 'new',
        }

    @api.depends_context('uid')
    def _compute_appointement_count(self):
        for record in self:
            record.appointement_count = self.env['hospital.appointement'].search_count([('patient_id', '=', record.id)])

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year - (
                        (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            else:
                rec.age = 0
        #
        # @api.model
        # def create(self, vals):
        #     patient = super(HospitalPatient, self).create(vals)
        #     if patient.email:
        #         patient.send_welcome_email()
        #     return patient
        #
        # def send_welcome_email(self):
        #     template_id = self.env.ref('hospital_management.email_template_patient_welcome').id
        #     self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
