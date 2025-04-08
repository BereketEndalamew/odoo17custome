from odoo import models, fields, api
from odoo.exceptions import UserError


class PersonalInformation(models.Model):
    _name = 'manager.reject'
    _description = 'Rejected Information'

    employe_id = fields.Many2one('personal.info', string="Employee Name", required=True)
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    country_id = fields.Char(string="Country", default='Ethiopia')
    state_id = fields.Char(string="State/Region")
    city_id = fields.Char(string="City")

    country_ids = fields.Char(string="Destination Country", default='Ethiopia')
    state_ids = fields.Char(string="Destination State/Region")
    city_ids = fields.Char(string="Destination City")

    request_date = fields.Date(string="Request Date", required=True)
    duration_date = fields.Date(string='Duration Date')

    travel_type = fields.Selection([
        ('toyota', 'Toyota'),
        ('pickup', 'PickUp'),
        ('vitz', 'Vitz'),
        ('bus', 'Bus')
    ], string="Travel Type")

    num_days = fields.Integer(string="Number of Days", compute='_compute_num_days', store=True)
    no_of_travellers = fields.Integer(string="Number of Travellers", readonly=True)

    traveller_ids = fields.One2many(
        'travel.traveller',
        'request_id',
        string="Travelers"
    )

    request_status = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('checked', 'Checked'),
    ], string="Request Status", default='checked', tracking=True)

    @api.depends('request_date', 'duration_date')
    def _compute_num_days(self):
        for record in self:
            if record.request_date and record.duration_date:
                record.num_days = (record.duration_date - record.request_date).days
            else:
                record.num_days = 0
