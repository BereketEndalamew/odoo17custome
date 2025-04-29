# models.py

from odoo import models, fields, api, _

class StoreIssueVoucher(models.Model):
    _name = 'store.issue.voucher'
    _description = 'Store Issue Voucher'

    # requester_id = fields.Many2one('res.users', string='Requested by', default=lambda self: self.env.user)
    name = fields.Char(string='Name', required=True, readonly=True, copy=False, default=lambda self: _('New'))
    effective_date = fields.Date(string='Effective Date', required=True, default=fields.Date.today())
    # date = fields.Date(string='Date', required=True, default=fields.Date.today())
    destination_location_id = fields.Many2one('stock.location', string='Destination Location')
    request_id = fields.Many2one('store.request', string='Store Request', readonly=True)
    is_equipment = fields.Boolean(default=False)
    eq_request_id = fields.Many2one('equipment.request', string="Equipment Request")
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    location_id = fields.Many2one('stock.location', string='Location', related='warehouse_id.view_location_id')
    issued_by = fields.Many2one('res.users', string='Issued by', readonly=True)
    issued_date = fields.Date(string='Issued Date', required=True, readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved by', readonly=True)
    approved_date = fields.Date(string='Approved Date', required=True, readonly=True)
    recieved_by = fields.Many2one('res.users', string='Recieved by')
    recieved_date = fields.Date(string='Recieved Date', readonly=True)
    voucher_lines = fields.One2many('store.issue.voucher.line', 'voucher_id', string='Voucher Lines')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approve', 'Approve'),
        ('validate', 'Validate')
    ], default="draft")

    stock_pick_count = fields.Integer(string='Stock Pick Count', compute='_compute_stock_pick_count')

    def _compute_stock_pick_count(self):
        for rec in self:
            rec.stock_pick_count = self.env['stock.picking'].search_count([('origin', '=', rec.name)])

    def stock_pick_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'stock pick',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.name)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

    def action_submit(self):
        self.state = 'submit'
        self.issued_by = self.env.user
        self.issued_date = fields.Date.today()


    def action_approve(self):
        self.state = 'approve'
        self.approved_by = self.env.user
        self.approved_date = fields.Date.today()

    def action_validate(self):
        self.state = 'validate'

    def create_transfer(self):
        stock_moves = []
        for line in self.voucher_lines:
            stock_move_vals = {
                'name': self.name,
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.quantity,
                'origin': self.name,
                'location_id': self.location_id.id if self.location_id else False,
                'location_dest_id': self.destination_location_id.id
            }
            stock_moves.append((0, 0, stock_move_vals))

        if stock_moves:
            stock_picking = self.env['stock.picking'].create({
                'location_id': self.location_id.id if self.location_id else False,
                'location_dest_id': self.destination_location_id.id,
                'picking_type_id': self.env.ref('stock.picking_type_out').id if self.env.ref('stock.picking_type_out', raise_if_not_found=False) else False,
                'move_ids_without_package': stock_moves,
                'origin': self.name,
            })
            stock_picking.action_confirm()
            stock_picking.action_assign()
            # stock_picking.button_validate()

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('store.issue.voucher') or _('New')
            res = super(StoreIssueVoucher, self).create(vals)
            return res

class StoreIssueVoucherLine(models.Model):
    _name = 'store.issue.voucher.line'
    _description = 'Store Issue Voucher Line'

    voucher_id = fields.Many2one('store.issue.voucher', string='Voucher')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
