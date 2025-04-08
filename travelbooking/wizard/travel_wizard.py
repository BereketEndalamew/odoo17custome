# from odoo import models, fields, api
# from odoo.exceptions import ValidationError
# from datetime import date, timedelta
# from datetime import datetime
# from odoo.exceptions import UserError
#
#
# class TravelWizard(models.TransientModel):
#     _name = 'travel.wizard'
#     _description = 'Travel Wizard'
#
#     employe_id = fields.Many2one('personal.info', string='Full Name', required=True)
#     phone = fields.Char(related='employe_id.phone', string='Phone', readonly=True)
#     email = fields.Char(related='employe_id.email', string='Email', readonly=True)
#
#     #
#     request_date = fields.Date(string="Request Date", required=True)
#     duration_date = fields.Date(string='Duration Date')
#     # no_of_travel = fields.Integer(string="No of Travel")
#     travel_type = fields.Selection([
#         ('toyota', 'Toyota'),
#         ('pickup', 'PickUp'),
#         ('vitz', 'Vitz'),
#         ('bus', 'Bus')
#     ], string="Travel Type")
#     num_days = fields.Integer(string="Number of Days", compute='_compute_num_days', store=True)
#     traveller_ids = fields.One2many('travel.traveller', 'request_id', string="Travelers")
#     no_of_travellers = fields.Integer(string="Number of Travelers", compute='_compute_no_of_travellers', store=True)
#
#     @api.depends('traveller_ids')
#     def _compute_no_of_travellers(self):
#         """Compute the number of travelers dynamically."""
#         for rec in self:
#             rec.no_of_travellers = len(rec.traveller_ids)
#
#     @api.depends('request_date', 'duration_date')
#     def _compute_num_days(self):
#         for rec in self:
#             if rec.request_date and rec.duration_date:
#                 # Convert the date strings to date objects
#                 request_date = fields.Date.from_string(rec.request_date)
#                 duration_date = fields.Date.from_string(rec.duration_date)
#                 # Calculate the difference in days
#                 rec.num_days = (duration_date - request_date).days
#             else:
#                 rec.num_days = 0
#
#     #
#     def travelbooking(self):
#         vals = {
#             'employe_id': self.employe_id.employe_id.id,  # Correct reference
#             'phone': self.phone,
#             'email': self.email,
#             'request_date': self.request_date,
#             'duration_date': self.duration_date,
#             'num_days': self.num_days,
#             'no_of_travellers': self.no_of_travellers,
#             'traveller_ids': [(0, 0, {
#                 'name': traveller.name,
#                 'phone': traveller.phone,
#                 'email': traveller.email,
#             }) for traveller in self.traveller_ids]
#         }
#
#         # Create a new record in the 'manager.approve' model
#         self.env['manager.approve'].create(vals)
#
#     @api.depends('request_date', 'duration_date')
#     def _compute_num_days(self):
#         for rec in self:
#             if rec.request_date and rec.duration_date:
#                 # Convert the date strings to date objects
#                 request_date = fields.Date.from_string(rec.request_date)
#                 duration_date = fields.Date.from_string(rec.duration_date)
#                 # Calculate the difference in days
#                 rec.num_days = (duration_date - request_date).days
#             else:
#                 rec.num_days = 0
#
#     @api.constrains('request_date', 'duration')
#     def _check_request_date(self):
#         for record in self:
#             if record.request_date < date.today():
#                 raise ValidationError("Request Date cannot be in the past. Please select a future date.")
#
#             if record.duration <= 0:
#                 raise ValidationError("Duration must be a positive number.")
#
#             if (record.request_date + timedelta(days=record.duration)) < record.request_date:
#                 raise ValidationError("The travel duration must be after the request date.")
#
#
# class TravelTraveller(models.TransientModel):
#     _name = 'travel.traveller'
#     _description = 'Travelers Information'
#     _rec_name = 'employe_id'
#
#     employe_id = fields.Many2one('hr.employee', string='Employe', required=True)
#     email = fields.Char(related='employe_id.email', string='Email Address')
#     phone = fields.Char(related='employe_id.phone', required=True)
#     request_id = fields.Many2one('travel.wizard', string="Travel Request")
