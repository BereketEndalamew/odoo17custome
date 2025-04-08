from odoo import api, models, fields

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    fname = fields.Char(string="Father's Name")  # Custom field for father's name
    product_uom_qty = fields.Char(string="Bereket Quantity")  # Custom field for product quantity

