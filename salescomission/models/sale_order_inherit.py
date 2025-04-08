from odoo import api, models, fields


# Sale Order Inheritance to create commission when confirmed
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        for order in self:
            # Checking if the salesperson (user_id) is assigned to the order
            if order.user_id:  # user_id refers to the salesperson in sale order
                # Creating the commission record
                self.env['sale.commission'].create({
                    'salesperson_id': order.user_id.id,  # Assigning the salesperson
                    'sale_order_id': order.id,  # Link to the confirmed sale order
                    'commission_amount': order.amount_untaxed * 0.05,  # 5% of untaxed amount
                    'date': order.date_order,  # Commission date same as sale order date
                    'state': 'draft',  # Initial state is 'draft'
                })
        return res
