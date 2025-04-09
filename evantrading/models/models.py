from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    cancelled_order_count = fields.Integer(
        string='Cancelled Orders',
        compute='_compute_cancelled_order_count'
    )

    @api.depends('partner_id')
    def _compute_cancelled_order_count(self):
        for record in self:
            # Count all cancelled purchase orders for the same partner
            record.cancelled_order_count = self.env['purchase.order'].search_count([
                ('state', '=', 'cancel')
            ])
    def action_view_cancelled_orders(self):
        return {
            'name': 'Cancelled Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('state', '=', 'cancel')],

        }
