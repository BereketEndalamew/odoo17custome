from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class StoreRequestPurchaseWizard(models.TransientModel):
    _name = 'store.request.purchase.wizard'
    _description = 'Store Request Purchase Wizard'

    store_request_id = fields.Many2one('store.request', string='Store Request', readonly=True)
    line_ids = fields.One2many('store.request.purchase.wizard.line', 'wizard_id', string='Products to Purchase')

    def action_create_purchase_request(self):
        PurchaseRequest = self.env['purchase.request']
        PurchaseRequestLine = self.env['purchase.request.line']
        if len(self.line_ids) <1:
            raise ValidationError(f"You need to have atleast one product fro creating Purchase Request")
        purchase_request = PurchaseRequest.create({
            'store_request_id': self.store_request_id.id,
            'state': 'to_approve',
            'checked_by': self.store_request_id.approved_by.id,
            'checked_date': self.store_request_id.approved_date,
        })

        for line in self.line_ids:
            if line.selected:
                PurchaseRequestLine.create({
                    'request_id': purchase_request.id,
                    'product_id': line.product_id.id,
                    'quantity': line.quantity_to_purchase,
                    'uom_id':line.uom_id.id
                })

        self.store_request_id.write({'state': 'on request'})
        return {'type': 'ir.actions.act_window_close'}

class StoreRequestPurchaseWizardLine(models.TransientModel):
    _name = 'store.request.purchase.wizard.line'
    _description = 'Store Request Purchase Wizard Line'

    wizard_id = fields.Many2one('store.request.purchase.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    requested_quantity = fields.Float(string='Requested Quantity', readonly=True)
    available_quantity = fields.Float(string='Available Quantity', readonly=True)
    quantity_to_purchase = fields.Float(string='Quantity to Purchase', readonly=True)
    selected = fields.Boolean(string='Select', default=True)
    uom_id= fields.Many2one('uom.uom', string='UOM', readonly=True)

class StoreRequestSIVWizard(models.TransientModel):
    _name = 'store.request.siv.wizard'
    _description = 'Store Request SIV Wizard'

    store_request_id = fields.Many2one('store.request', string='Store Request', readonly=True)
    line_ids = fields.One2many('store.request.siv.wizard.line', 'wizard_id', string='Products to Issue')

    def action_create_siv(self):
        StoreIssueVoucher = self.env['store.issue.voucher']
        StoreIssueVoucherLine = self.env['store.issue.voucher.line']
        if len(self.line_ids) <1:
            raise ValidationError(f"You need to have atleast one product fro creating SIV")
        siv = StoreIssueVoucher.create({
            'request_id': self.store_request_id.id,
            'issued_by': self.store_request_id.requester_id.user_id.id,
            'issued_date': self.store_request_id.requested_date,
            'approved_by': self.store_request_id.approved_by.id,
            'approved_date': self.store_request_id.approved_date,
        })

        for line in self.line_ids:
            if line.selected:
                StoreIssueVoucherLine.create({
                    'voucher_id': siv.id,
                    'product_id': line.product_id.id,
                    'quantity': line.quantity_to_issue,
                })

        self.store_request_id.write({'state': 'on siv'})
        return {'type': 'ir.actions.act_window_close'}

class StoreRequestSIVWizardLine(models.TransientModel):
    _name = 'store.request.siv.wizard.line'
    _description = 'Store Request SIV Wizard Line'

    wizard_id = fields.Many2one('store.request.siv.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    requested_quantity = fields.Float(string='Requested Quantity', readonly=True)
    available_quantity = fields.Float(string='Available Quantity', readonly=True)
    quantity_to_issue = fields.Float(string='Quantity to Issue')
    selected = fields.Boolean(string='Select', default=True)
    uom_id= fields.Many2one('uom.uom', string='UOM', readonly=True)

    @api.onchange('quantity_to_issue')
    def _onchange_quantity_to_issue(self):
        if self.quantity_to_issue > self.available_quantity:
            self.quantity_to_issue = self.available_quantity
        elif self.quantity_to_issue > self.requested_quantity:
            self.quantity_to_issue = self.requested_quantity
