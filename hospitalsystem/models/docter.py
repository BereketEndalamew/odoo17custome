from odoo import api, models, fields
from odoo.fields import Many2one


class hospitalDocter(models.Model):
    _name = 'hospital.docter'
    _description = 'Hospital Docter Page'

    # #
    docter_id = fields.Many2one('res.users', string='Docter')
    email = fields.Char(related='docter_id.login', string='Email Address')
    phone = fields.Char(string="Phone Number")
    image = fields.Image(string='Image')
    patient_count = fields.Integer(string="Number of Patients", compute='_compute_patient_count')

    @api.depends('docter_id')
    def _compute_patient_count(self):
        for rec in self:
            rec.patient_count = self.env['hospital.appointement'].search_count([('docter_id', '=', rec.docter_id.id)])

    def viewPatients(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'View My Patients',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointement',
            'domain': [('docter_id', '=', self.docter_id.id)],
            'target': 'self',
        }
