# models.py
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo import models, fields, api, _

class EquipmentRequest(models.Model):
    _name = 'equipment.request'
    _description = 'Equipment Borrow Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    requested_date = fields.Date(string='Request date', required=True, default=fields.Date.today())
    return_date = fields.Date(string='Return date', required=True, default=fields.Date.today())
    request_lines = fields.One2many('equipment.request.line', 'request_id', string='Request Lines')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    # location_id = fields.Many2one('stock.location', string='Location', related='warehouse_id.view_location_id')
    requester_id = fields.Many2one('hr.employee', string='Requested by', default = lambda self:self.env.user.employee_id.id)
    department_id = fields.Many2one('hr.department', related="requester_id.department_id")
    # destination_location_id = fields.Many2one('stock.location', string='Destination Location', required=True)
    reason = fields.Char(string="Reason")
    ref = fields.Char(string="Reference")
    state = fields.Selection([
        ('draft','Draft'),
        ('to_approve','To Approve'),
        ('reject','Reject'),
        ('approved', 'Approved'),
        ('validate','Validate'),
        ('on request', 'on request'),
        ('on siv', 'on siv')
    ], default="draft")
    siv_count = fields.Integer(string='SIV Count', compute='_compute_siv_count')
    pr_count = fields.Integer(string='Purchase Request Count', compute='_compute_pr_count')
    approved_by = fields.Many2one('res.users', string="Approved by",  readonly=True, compute='_compute_approved_by', store=True)
    approved_date = fields.Date(string="Approved Date")
    is_allowed = fields.Boolean(string="Is Allowed To write", default=False, compute="_is_allowed_check")
    
    def _is_allowed_check(self):
        self.is_allowed = self.env.user.has_group('pre_mrp.group_shift_leader')

    def _compute_siv_count(self):
        for rec in self:
            rec.siv_count = self.env['store.issue.voucher'].search_count([('eq_request_id', '=', rec.id)])

    # def _compute_pr_count(self):
    #     for rec in self:
    #         rec.pr_count = self.env['purchase.request'].search_count([('store_request_id', '=', rec.id)])

    # def pr_action(self):

    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Purchase Request',
    #         'res_model': 'purchase.request',
    #         'domain': [('store_request_id', '=', self.id)],
    #         'view_mode': 'tree,form',
    #         'target': 'current'
    #     }

    def siv_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'store issue',
            'res_model': 'store.issue.voucher',
            'domain': [('eq_request_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

    def action_submit(self):
        if any(line.quantity <= 0 for line in self.request_lines):
            raise ValidationError("Equipment Quantity to request can not be empty")
        self.state = 'to_approve'

    def action_approve(self):
        self.state = 'approved'
        self.approved_by = self.env.user
        self.approved_date = datetime.today()

    def action_reject(self):
        self.state = 'reject'

    # def create_purchase_request(self):
    #     PurchaseRequest = self.env['purchase.request']
    #     PurchaseRequestLine = self.env['purchase.request.line']
    #     for request in self:
    #         if request.state=="approved":
    #             request.state = "on request"
    #             purchase_request = PurchaseRequest.create({
    #                 'store_request_id': request.id,
    #             })
    #             for line in request.request_lines:
    #                 PurchaseRequestLine.create({
    #                     'request_id': purchase_request.id,
    #                     'product_id': line.product_id.id,
    #                     'quantity': line.quantity,
    #                     # 'unit_price': line.unit_price
    #                 })

    
    def create_issue_voucher(self):
        StoreIssueVoucher = self.env['store.issue.voucher']
        StoreIssueVoucherLine = self.env['store.issue.voucher.line']
        for request in self:
            if request.state=="approved":
                request.state = "on siv"
            else:
                continue
            issue_voucher = StoreIssueVoucher.create({
                'eq_request_id': request.id,
                'is_equipment':True,
               'issued_by': request.requester_id.user_id.id,
                'issued_date': request.requested_date,
                'approved_by': request.approved_by.id,
                'approved_date': request.approved_date or datetime.today(),
                'voucher_lines': [(0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                }) for line in request.request_lines if line.qty_available > 0]
            })
            for line in request.request_lines:
                StoreIssueVoucherLine.create({
                    'voucher_id': issue_voucher.id,
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                })

                self.env['equipment.issue'].create({
                'name': self.env['ir.sequence'].next_by_code('equipment.issue') or _('New'),
                'equipment_request_id': request.id,  # Adjust based on your logic
                'requested_date': self.requested_date,
                'return_date': self.return_date,
                'reason': self.reason,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
            })

    def create_issue_and_voucher(self):
        self.create_issue_voucher()
        self.create_purchase_request()

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('equipment.request') or _('New')
            res = super(EquipmentRequest, self).create(vals)
            return res
    @api.constrains('request_lines')
    def _check_request_lines(self):
        for record in self:
            if not record.request_lines:
                raise ValidationError("At least one line is required in Request Lines.")
class EquipmentRequestLine(models.Model):
    _name = 'equipment.request.line'
    _description = 'Equipment Request Line'

    sequence = fields.Integer(string='SN', default="10")

    request_id = fields.Many2one('equipment.request', string='Equipment Request')
    product_id = fields.Many2one('product.product', string='Product/Description', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1.00)
    qty_available = fields.Float( string="On-Hand Quantity", related='product_id.qty_available', readonly=True )
    # unit_price = fields.Float(string="Unit Price", default=False, required=True) 
    uom_id = fields.Many2one('uom.uom', related="product_id.uom_po_id")
    remark = fields.Char(string="Remark")

    _order = 'request_id, sequence'

    @api.model
    def create(self, values):
        if 'sequence' not in values:
            values['sequence'] = self._get_last_sequence(values.get('request_id')) + 1
        return super(EquipmentRequestLine, self).create(values)

    def _get_last_sequence(self, request_id):
        last_line = self.search([('request_id', '=', request_id)], order='sequence desc', limit=1)
        return last_line.sequence if last_line else 0
    
    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 1:
                raise ValidationError("Quantity must be at least 1.")
            
    # @api.depends('state')
    # def _compute_approved_by(self):
    #     for record in self:
    #         if record.state == 'approve':
    #             record.approved_by = self.env.user
    #         else:
    #             record.approved_by = False        