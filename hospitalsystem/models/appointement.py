from odoo import models, fields, api
from datetime import date, datetime


class HospitalAppointement(models.Model):
    _name = 'hospital.appointement'  # Corrected model name
    _description = 'Hospital Appointement'  # Corrected description

    image = fields.Image(string='Image')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    age = fields.Integer(related='patient_id.age', string='Age', readonly=True)
    gender = fields.Selection(related='patient_id.gender', string='Gender', readonly=True)
    phone = fields.Char(related='patient_id.phone', string='Phone', readonly=True)
    docter_id = fields.Many2one('res.users', string='Docter')
    email = fields.Char(related='patient_id.email', string='Email', readonly=True)
    appointement_date = fields.Date(string="Appointement Date", required=True)
    appointement_count = fields.Integer(string="Appointement Count", compute="_compute_count")
    prescription = fields.Html(string='Prescription')
    pharmacy_id = fields.One2many('hospital.pharmacy', 'appointement_id',
                                  string='Pharmacy Id')  # Corrected One2many field


    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], string="Priority")
    state2 = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default="draft", tracking=True)

    state1 = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')  # added default value
    draft_count = fields.Integer(string='Draft', compute='_compute_counts')
    done_count = fields.Integer(string='Done', compute='_compute_counts')
    cancel_count = fields.Integer(string='Cancel', compute='_compute_counts')
    in_consultation_count = fields.Integer(string='In Consultation', compute='_compute_counts')


    def Appointements(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'View My Patients',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointement',
            'domain': [('sate1', '=', self.state1.id)],
            'target': 'new',
        }


    @api.depends()
    def _compute_counts(self):
        for rec in self:
            rec.draft_count = self.search_count([('state1', '=', 'draft')])
            rec.done_count = self.search_count([('state1', '=', 'done')])
            rec.cancel_count = self.search_count([('state1', '=', 'cancel')])
            rec.in_consultation_count = self.search_count([('state1', '=', 'in_consultation')])


    @api.depends()
    def _compute_count(self):
        for record in self:  # Added loop
            record.appointement_count = self.env['hospital.appointement'].search_count([])  # corrected search


    def action_in_consultation(self):
        for rec in self:
            rec.state1 = 'in_consultation'


    def action_draft(self):
        for rec in self:
            rec.state1 = 'draft'


    def action_done(self):
        for rec in self:
            rec.state1 = 'done'


    def action_cancel(self):
        for rec in self:
            rec.state1 = 'cancel'


class HospitalPharmacy(models.Model):
    _name = 'hospital.pharmacy'
    _description = 'Hospital Pharmacy'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    amount = fields.Float(string='Amount', required=True, default=1)
    price = fields.Float(string='Price')
    appointement_id = fields.Many2one('hospital.appointement', string='Appointement Id',
                                      required=True)  # Corrected Many2one field
