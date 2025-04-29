from datetime import date
from odoo import models, fields, api, _

class EquipmentIssue(models.Model):
    _name = 'equipment.issue'
    _description = 'Equipment Issue'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    equipment_request_id = fields.Many2one('equipment.request', string='Equipment Request', required=True)
    requested_date = fields.Date(string='Request Date', required=True, default=fields.Date.today)
    return_date = fields.Date(string='Return Date', required=True)
    reason = fields.Char(string="Reason")
    product_id = fields.Many2one('product.product', string="Product", required=True, readonly=True)
    quantity = fields.Float(string="Quantity", required=True, readonly=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('issue', 'Issued'),
        ('returned', 'Returned'),
        ('pending', 'Pendng'),
        ('late', 'Late'),
    ], default="draft", tracking=True, readonly=True)

    def action_return(self):
        self.state = 'pending'
        self.env['store.issue.voucher'].return_transfer()

    def update_late_status(self):
        """Mark equipment issues as 'Late' if the return date has passed."""
        overdue_issues = self.search([('state', 'not in', ['returned', 'late']), ('return_date', '<', date.today())])
        for issue in overdue_issues:
            issue.state = 'late'