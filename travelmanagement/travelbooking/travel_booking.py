from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class EmployeWizard(models.Model):
    _name = 'employe.wizard'
    _description = 'Travel Wizard'
    # _rec_name = 'employe_id'

    employe_id = fields.Many2one('hr.employee', string='Employe', required=True)
    email = fields.Char(related='employe_id.work_email', string='Email Address')
    phone = fields.Char(related='employe_id.mobile_phone', string="Phone Number")

    request_date = fields.Date(string="Request Date", required=True)
    end_date = fields.Date(string='Return Date')
    approved_date = fields.Datetime(string="Approved Date")
    request_status = fields.Selection([
        ('draft', 'Draft'),
        ('checked', 'Checked'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Request Status", default='draft')

    travel_type = fields.Selection([
        ('toyota', 'Toyota'),
        ('pickup', 'PickUp'),
        ('vitz', 'Vitz'),
        ('bus', 'Bus')
    ], string="Travel Type")

    num_days = fields.Integer(string="Number of Days", compute='_compute_num_days', store=True)
    traveller_ids = fields.One2many('travel.cotraveller', 'request_id', string="Travelers")
    no_of_travellers = fields.Integer(string="Number of Travelers", compute='_compute_no_of_travellers', store=True)

    @api.constrains('request_date', 'end_date')
    def _check_dates(self):
        for record in self:
            today = date.today()
            if record.request_date and record.request_date < today:
                raise ValidationError("Request Date cannot be in the past.")
            if record.end_date and record.end_date < today:
                raise ValidationError("Return Date cannot be in the past.")
            if record.end_date and record.request_date and record.end_date < record.request_date:
                raise ValidationError("Return Date cannot be earlier than Request Date.")

    @api.depends('traveller_ids')
    def _compute_no_of_travellers(self):
        """Compute the number of travelers dynamically."""
        for rec in self:
            rec.no_of_travellers = len(rec.traveller_ids)

    @api.depends('request_date', 'end_date')
    def _compute_num_days(self):
        for rec in self:
            if rec.request_date and rec.end_date:
                rec.num_days = (rec.end_date - rec.request_date).days
            else:
                rec.num_days = 0


    def travelwizard(self):
        self.ensure_one()
        self.write({'request_status': 'draft'})  # Optional, to enforce consistency
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manager Approval',
            'res_model': 'employe.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current'
        }


    def action_create_request(self):
        self.ensure_one()
        self.request_status = "checked"


    def action_checked(self):
        self.write({'request_status': 'checked'})
        self.request_status = "approved"


    def action_approve(self):
        self.write({'request_status': 'approved',
                    'approved_date': fields.Datetime.now()})


    def action_reject(self):
        self.write({'request_status': 'rejected'})

    def create(self, vals):
        if vals.get('request_status') in ['checked', 'approved', 'rejected']:
            raise ValidationError("You cannot create a new request directly in Checked, Approved, or Rejected status.")
        return super().create(vals)



class TravelTraveller(models.TransientModel):
    _name = 'travel.cotraveller'
    _description = 'Travelers Information'

    employe_id = fields.Many2one('hr.employee', string='Employe', required=True)
    email = fields.Char(related='employe_id.work_email', string='Email Address')
    phone = fields.Char(related='employe_id.mobile_phone', string="Phone Number")
    request_id = fields.Many2one('employe.wizard', string="Travel Request")
