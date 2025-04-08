# from odoo import models, fields, api
# from odoo.exceptions import UserError
# from datetime import date
#
#
# class EmployeInformation(models.Model):
#     _name = 'employe.travel'
#     _description = 'Request Information'
#
#     employe_id = fields.Many2one('hr.employee', string='Employe')
#     email = fields.Char(related='employe_id.work_email', string='Email Address')
#     phone = fields.Char(related='employe_id.mobile_phone', string="Phone Number")
#     request_date = fields.Date(string="Request Date")
#     duration_date = fields.Date(string='Duration Date')
#     # no_of_travel = fields.Integer(string="No of Travel")
#     travel_type = fields.Selection([
#         ('toyota', 'Toyota'),
#         ('pickup', 'PickUp'),
#         ('vitz', 'Vitz'),
#         ('bus', 'Bus')
#     ], string="Travel Type")
#     num_days = fields.Integer(string="Number of Days", compute='_compute_num_days', store=True)
#     no_of_travellers = fields.Integer(string="Number of Travellers", readonly=True)  # Add this field
#     traveller_ids = fields.One2many(
#         'travel.traveller',
#         'request_id',
#         string="Travelers")
#     # # Only include travelers linked to a request
#
#     request_status = fields.Selection([
#         ('draft', 'Draft'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#         ('checked', 'Checked'),
#     ], string="Request Status", default='draft', tracking=True)
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
#                 @api.depends('traveller_ids')
#                 def _compute_no_of_travellers(self):
#                     """Compute the number of travelers dynamically."""
#                     for rec in self:
#                         rec.no_of_travellers = len(rec.traveller_ids)
#
#     @api.depends('request_date', 'duration_date')
#
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
#     def open_wizard(self):
#         """Open a wizard to create an Employee Travel Request"""
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Employee Registration Page',
#             'view_mode': 'form,tree',
#             'res_model': 'employe.travel',
#             'context': {'default_employe_id': self.employe_id.id},
#             'target': 'new',
#         }
#
#     def action_checked(self):
#         """Move the request to 'Checked' status"""
#         if self.request_status == 'draft':
#             self.write({'request_status': 'checked'})
#
#     def action_approved(self):
#         """Move the request to 'Approved' status"""
#         if self.request_status == 'checked':  # Only move forward if it's 'checked'
#             self.write({'request_status': 'approved'})
#
#     def action_rejected(self):
#         """Move the request to 'Rejected' status"""
#         if self.request_status in ['draft', 'checked']:  # Can reject from draft or checked
#             self.write({'request_status': 'rejected'})
#
#
# class TravelTraveller(models.TransientModel):
#     _name = 'travel.traveller'
#     _description = 'Travelers Information'
#
#     employe_id = fields.Many2one('hr.employee', string='Employe', required=True)
#     email = fields.Char(related='employe_id.work_email', string='Email Address')
#     phone = fields.Char(related='employe_id.mobile_phone', string="Phone Number")
#     request_id = fields.Many2one('employe.travel', string="Travel Request")
