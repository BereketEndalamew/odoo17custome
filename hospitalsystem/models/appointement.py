from odoo import models, fields, api


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
    appointement_date = fields.Datetime(string="Appointement Date", required=True)
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
    price = fields.Float( string='Price')
    appointement_id = fields.Many2one('hospital.appointement', string='Appointement Id',
                                      required=True)  # Corrected Many2one field
