from odoo import api, models, fields

# Sales Commission Model
class SaleCommission(models.Model):
    _name = 'sale.commission'
    _description = 'Calculating Sales Commission'

    salesperson_id = fields.Many2one('res.users', string='Salesperson', required=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    commission_amount = fields.Float(string='Commission Amount', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('paid', 'Paid')
    ], string='State', default='draft')

