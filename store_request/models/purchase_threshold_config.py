from odoo import api,fields,models,_ 
from odoo.exceptions import UserError,ValidationError

class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    direct_purchase_threshold = fields.Float(string="Direct Purchase Threshold", default=1.0)
    proforma_purchase_threshold = fields.Float(string="PreForma Purchase Threshold", default=5000.0)
    bid_purchase_threshold = fields.Float(string="Bid Purchase Threshold", default=20000.0)

    @api.model
    def get_values(self):
        res = super(PurchaseConfigSettings, self).get_values()
        res.update(
            direct_purchase_threshold=float(self.env['ir.config_parameter'].sudo().get_param('purchase.direct_purchase_threshold', default=1.0)),
            proforma_purchase_threshold=float(self.env['ir.config_parameter'].sudo().get_param('purchase.proforma_purchase_threshold', default=5000.0)),
            bid_purchase_threshold=float(self.env['ir.config_parameter'].sudo().get_param('purchase.bid_purchase_threshold', default=20000.0)),
        )
        return res

    def set_values(self):
        super(PurchaseConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('purchase.direct_purchase_threshold', self.direct_purchase_threshold)
        self.env['ir.config_parameter'].sudo().set_param('purchase.proforma_purchase_threshold', self.proforma_purchase_threshold)
        self.env['ir.config_parameter'].sudo().set_param('purchase.bid_purchase_threshold', self.bid_purchase_threshold)
