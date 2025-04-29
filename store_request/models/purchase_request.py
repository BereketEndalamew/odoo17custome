from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    vendor_id = fields.Many2one('res.partner', string="Vendor",)
    store_request_id = fields.Many2one('store.request', string='Store Request', required=True)
    effective_date = fields.Date(string='Effective Date', required=True, default=fields.Date.today())
    request_lines = fields.One2many('purchase.request.line', 'request_id', string='Request Lines')
    purchase_tender_count = fields.Integer(string='Purchase Tender Count', compute='_compute_purchase_tender_count')

    approved_by = fields.Many2one('res.users', string="Approved by",  readonly=True, store=True)
    approved_date = fields.Date(string='Approval Date', readonly=True,)

    checked_by = fields.Many2one('res.users', string="Checked by",  readonly=True, store=True)
    checked_date = fields.Date(string='Checked Date', readonly=True,)

    market = fields.Selection([
        ('local', 'Local'),
        ('local_addis_ababa', 'Local Addis Ababa'),
        ('abroad', 'Abroad'),
    ], string="Market", default="local")

    transportation = fields.Selection([
        ('land', 'Land'),
        ('air', 'Air'),
        ('sea', 'Sea'),
    ], string="Transportation", default="land")

    urgency = fields.Selection([
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ], string="Urgency", default="routine")

    show_validate_button = fields.Boolean(string="Show Validate Button", compute="_compute_show_validate_button")

    # compute number of purchase orders for the purchase requested
    purchase_order_count = fields.Integer(string='Purchase Order Count', compute='_compute_purchase_order_count')

    purchase_type = fields.Selection([
        ('direct', 'DIRECT'),
        ('proforma', 'PROFORMA'),
        ('bid', 'BID')
    ], default="direct", compute="_get_purchase_type", store=True)

    @api.depends('request_lines.quantity', 'request_lines.unit_price')
    def _get_purchase_type(self):
        for rec in self:
            total_amount = sum(line.quantity * line.current_market_price for line in rec.request_lines)
            
            # Get threshold values from system parameters
            IrConfig = self.env['ir.config_parameter'].sudo()
            direct_threshold = float(self.env['ir.config_parameter'].sudo().get_param('purchase.direct_purchase_threshold', default=20000))
            proforma_threshold = float(   self.env['ir.config_parameter'].sudo().get_param('purchase.proforma_purchase_threshold', default=20000))
            bid_threshold = float(   self.env['ir.config_parameter'].sudo().get_param('purchase.bid_purchase_threshold', default=20000))

            # Determine purchase type based on total amount
            if total_amount < proforma_threshold:
                rec.purchase_type = 'direct'
            elif total_amount >= proforma_threshold and total_amount < bid_threshold:
                rec.purchase_type = 'proforma'
            elif total_amount > bid_threshold:
                rec.purchase_type = 'bid'

    def action_open_purchase_tender_transit(self):
        # This method triggers the action when the button is clicked
        return {
            'type': 'ir.actions.act_window',
            'name': 'Winners',
            'res_model': 'purchase.tender.transit',
            'domain': [('request_id', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current',  # This makes it open in the same window
        }

    def _compute_purchase_order_count(self):
        for rec in self:
            rec.purchase_order_count = self.env['purchase.order'].search_count([('ref', '=', rec.name),('state', '!=', 'cancel'), ('tender_status', '=', False)])

    def purchase_order_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'res_model': 'purchase.order',
            'domain': [('ref', '=', self.name),('tender_status', '=', False)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

   
    def _compute_purchase_tender_count(self):
        for rec in self:
            rec.purchase_tender_count = self.env['purchase.tender'].search_count([('request_id', '=', rec.name)])

    def purchase_tender_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Tender',
            'res_model': 'purchase.tender',
            'domain': [('request_id', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('on request', 'On Request'),
        ('done', 'Done'),
        ('validate', 'Validate'),
        ('tender', 'Tender Created'),
        ('direct_purchase', 'Direct Purchase')
    ], default="draft")

    def action_submit(self):
        self.state = 'to_approve'
        self.checked_by = self.env.user
        self.checked_date = fields.Date.today()

    def action_approve(self):
        self.state = 'approved'
        self.approved_by = self.env.user
        self.approved_date = fields.Date.today()
        self.set_product_price()
    
    def set_product_price(self):
        for rec in self:
            for line in rec.request_lines:
                line.product_id.standard_price = line.current_market_price

    def action_validate(self):
        self.state = 'validate'

    def reset_draft(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or _('New')
            res = super(PurchaseRequest, self).create(vals)
            return res
            return res

    def create_purchase_tender(self):
        # List to store products for which tenders are already created
        existing_tender_products = []

        for line in self.request_lines:
            # Check if a tender already exists for the product
            existing_tender = self.env['purchase.tender'].search([
                ('product_id', '=', line.product_id.id),
                ('request_id', '=', self.name)
            ], limit=1)

            if existing_tender:
                existing_tender_products.append(line.product_id.name) 
                
                continue  
            # Create a new tender if it doesn't already exist
            tender_vals = {
                'request_id': self.name,
                'product_id': line.product_id.id,
                'tender_line_ids': [(0, 0, {
                    'product_qty': line.quantity,
                    'product_uom': line.product_id.uom_id.id,
                })]
            }
            self.env['purchase.tender'].create(tender_vals)
        self.state = 'tender'

        # If all products in request_lines have tenders created, raise a validation error
        if len(existing_tender_products) == len(self.request_lines):
            raise ValidationError(_("Tenders have already been created for all products: %s") % ', '.join(existing_tender_products))

    def action_create_purchase_order(self):
        if not self.vendor_id:
            raise UserError("Please provide a vendor before creating the purchase order.")
        
        config_param = self.env['ir.config_parameter'].sudo()
        max_direct_purchase = float(config_param.get_param('purchase.max_direct_purchase', default=5000))

        # Add validation if total_price > max_direct_purchase and tender_id is empty
        # for line in self.request_lines:
        #     if line.unit_price > max_direct_purchase:
        #         raise ValidationError(f"Costs for {line.product_id.name} are too high for a direct purchase. Please create a tender.")

        self.env['purchase.order'].create({
            'ref': self.name,
            'partner_id': self.vendor_id.id,
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.quantity,
                'price_unit': line.current_market_price,
            }) for line in self.request_lines],
        })

        self.state = 'direct_purchase'

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string='Purchase Request')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    unit_price = fields.Float(string="Unit Price(old)", related='product_id.standard_price') 
    uom_id = fields.Many2one('uom.uom', related="product_id.uom_po_id")
    remark = fields.Char(string="Remark")
    current_market_price= fields.Float(string="Current Price", default=lambda self: self.unit_price, copy=False)

    @api.depends('current_market_price')
    def _set_product_price(self):
        for record in self:
            record.product_id.standard_price = record.current_market_price
