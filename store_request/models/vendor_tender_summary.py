from odoo import models, fields, api, _

class PurchaseTenderTransit(models.Model):
    _name = 'purchase.tender.transit'
    _description = 'Purchase Tender Transit'

    name = fields.Char(string='Name', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', readonly=True)
    product_count = fields.Integer(string='Products Won', readonly=True, compute='_compute_product_count')
    request_id = fields.Char(string='Request ID', readonly=True)
    tender_id = fields.Many2one('purchase.tender', string='Tender ID', readonly=True)
    transit_line_ids = fields.One2many('purchase.tender.transit.line', 'transit_id', string='Transit Lines', readonly=True)

    purchase_order_count = fields.Integer(string='Purchase Order Count', compute='_compute_purchase_order_count')

    def _compute_purchase_order_count(self):
        for rec in self:
            rec.purchase_order_count = self.env['purchase.order'].search_count([('partner_id', '=', self.vendor_id.id), ('transit_id', '=', rec.id)])

    def purchase_order_action(self):
        

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'domain': [('partner_id', '=', self.vendor_id.id), ('ref', '=', self.request_id)],
            'view_mode': 'tree,form',
            'target': 'current'
        }        

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.tender.transit') or _('New')
            res = super(PurchaseTenderTransit, self).create(vals)
            return res
        
    @api.depends('transit_line_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.transit_line_ids)

    def create_po_for_vendor(self):
            vendor_lines = self.transit_line_ids
            if vendor_lines:
                # Initialize order_lines outside of the loop
                order_lines = []
                for line in vendor_lines:
                    # Append each line to order_lines
                    order_lines.append((0, 0, {
                        'tender_id': line.tender_id.id,
                        'product_id': line.product_id.id,
                        'name': line.product_id.name,
                        'product_qty': line.product_qty,
                        'price_unit': line.price_unit,
                        # 'product_uom': line.product_uom.id,
                    }))
                
                # Prepare the order values with all order lines
                order_vals = {
                    'partner_id': self.vendor_id.id,
                    'ref': self.request_id,
                    'transit_id': self.id,
                    'order_line': order_lines
                }
                # Create the purchase order with the compiled order lines
                self.env['purchase.order'].create(order_vals)


class PurchaseTenderTransitLine(models.Model):
    _name = 'purchase.tender.transit.line'
    _description = 'Purchase Tender Transit Line'

    transit_id = fields.Many2one('purchase.tender.transit', string='Transit')
    tender_id = fields.Many2one('purchase.tender', string='Tender ID', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_qty = fields.Float(string='Quantity', readonly=True)
    product_uom = fields.Many2one('uom.uom', string='UOM', readonly=True)
    price_unit = fields.Float(string='Unit Price', readonly=True)
