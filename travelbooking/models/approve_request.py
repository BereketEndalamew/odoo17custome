from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class PersonalInformation(models.Model):
    _name = 'employe.travel'
    _description = 'Request Information'

    _rec_name = 'employe_id'
    employe_id = fields.Many2one('hr.employee', string='Employe', required=True)
    email = fields.Char(related='employe_id.email', string='Email Address')
    phone = fields.Char(related='employe_id.phone', required=True)
    request_date = fields.Date(string="Request Date", required=True)
    duration_date = fields.Date(string='Duration Date')
    # no_of_travel = fields.Integer(string="No of Travel")
    travel_type = fields.Selection([
        ('toyota', 'Toyota'),
        ('pickup', 'PickUp'),
        ('vitz', 'Vitz'),
        ('bus', 'Bus')
    ], string="Travel Type")
    num_days = fields.Integer(string="Number of Days", compute='_compute_num_days', store=True)
    no_of_travellers = fields.Integer(string="Number of Travellers", readonly=True)  # Add this field
    traveller_ids = fields.One2many(
        'travel.traveller',
        'request_id',
        string="Travelers")
    # Only include travelers linked to a request

    request_status = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('checked', 'Checked'),
    ], string="Request Status", default='checked', tracking=True)

    def action_approve(self):
        """Approve the travel request after validation"""
        for rec in self:
            if not rec.traveller_ids:
                raise UserError("I have not enough service!!!")

            rec.request_status = 'approved'
            self._send_email_notification('approved')

    def action_reject(self):
        """Move rejected records to manager.rejected and delete them from manager.approve."""
        for record in self:
            # Create a rejected record
            # vals = {
            #     'employe_id': self.employe_id.employe_id.id,  # Correct reference
            #     'phone': self.phone,
            #     'email': self.email,
            #     'request_date': self.request_date,
            #     'duration_date': self.duration_date,
            #     'num_days': self.num_days,
            #     'no_of_travellers': self.no_of_travellers,
            #     'traveller_ids': [(0, 0, {
            #         'name': traveller.name,
            #         'phone': traveller.phone,
            #         'email': traveller.email,
            #     }) for traveller in self.traveller_ids]
            # }
            #
            # # Create a new record in the 'manager.approve' model
            # self.env['manager.reject'].create(vals)

            # Delete the record from manager.approve
            record.unlink()
            self._send_email_notification('rejected')

        return True  # Successfully executed

    def _send_email_notification(self, status):
        """Send an email notification to the employee based on approval or rejection."""
        template_id = False
        if status == 'approved':
            template_id = self.env.ref('travelbooking.email_template_travel_request_approved')
        elif status == 'rejected':
            template_id = self.env.ref('travelbooking.email_template_travel_request_rejected')

        if template_id:
            template_id.send_mail(self.id, force_send=True)

    def open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employe Registration Page',
            'view_mode': 'form',
            'res_model': 'travel.wizard',
             'context': {'default_employe_id': self.employe_id.id},  # Prefill patient_id
            'target': 'new',
        }
