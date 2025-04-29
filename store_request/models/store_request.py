from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
class StoreRequest(models.Model):
    _name = 'store.request'
    _description = 'Store Request'
    

    name = fields.Char(string='Name', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    effective_date = fields.Date(string='Effective Date', required=True, default=fields.Date.today())
    requested_date = fields.Date(string='Request Date', readonly=True, required=True, default=fields.Date.today())
    request_lines = fields.One2many('store.request.line', 'request_id', string='Request Lines')
    # warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    # location_id = fields.Many2one('stock.location', string='Location', related='warehouse_id.view_location_id')
    requester_id = fields.Many2one('hr.employee', string='Requested by', default=lambda self: self.env.user.employee_id.id)
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

    approved_by = fields.Many2one('res.users', string="Approved by",  readonly=True, store=True)
    approved_date = fields.Date(string='Approval Date', readonly=True,)

    checked_by = fields.Many2one('res.users', string="Checked by",  readonly=True, store=True)
    checked_date = fields.Date(string='Checked Date', readonly=True,)
    is_allowed = fields.Boolean(string="Is Allowed To write",default=True, compute="_is_allowed_check", store=False)
    is_approver= fields.Boolean(string="Is Approver",default=False, compute="_is_approver", store=False)
    active = fields.Boolean(string="Is Active", default=True)
    can_siv = fields.Boolean(default=True, compute="_compute_can_siv")
    urgency = fields.Selection([
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
            ('very_urgent','Very Urgent')
        ], string='Urgency', default='medium')
    def _compute_can_siv(self):
        # ittrate over all the request_lines and check if there is an siv object with this store request ref, who have made teh transfer for.
        _logger.info(f"SR: {self.can_siv}")
        siv_created = self.env['store.issue.voucher'].search([
                ('request_id', '=', self.id)
            ])


        
        _logger.info(f"{len(siv_created)}")
        for siv in siv_created:
            _logger.info(f"SR: {len(siv.voucher_lines)}")
            for line in self.request_lines:
                _logger.info(f"SR: {line.product_id.name}")
                for i in siv.voucher_lines:
                    _logger.info(f"SR: {i.product_id.name} to {line.product_id.name} ")
                    if line.product_id.id == i.product_id.id:
                        _logger.info("is fullfiled")
                        line.fulfilled = True 

        
        _logger.info(f"SR: {all(line.fulfilled for line in self.request_lines)}")
        self.can_siv = not all(line.fulfilled for line in self.request_lines)
        _logger.info(f"SR: {self.can_siv}")

            

                
                    
                    
    def unlink(self):
        if self.state in ['approved','on_request','on_siv']:
            raise ValidationError('Can\'t delete a store request once it is approved')
        return super().unlink()
    

    @api.depends('requester_id')  # Only recompute when necessary
    def _is_approver(self):
        for rec in self:
            requester = rec.requester_id
            if requester and requester.department_id and requester.department_id.manager_id:
                rec.is_approver = self.env.user.id == requester.department_id.manager_id.user_id.id
            else:
                rec.is_approver = False


    @api.depends('state')  # Only recompute when necessary
    def _is_allowed_check(self):
        for rec in self:
            rec.is_allowed = True
    def _compute_siv_count(self):
        _logger.info("siv count")
        for rec in self:
            rec.siv_count = self.env['store.issue.voucher'].search_count([('request_id', '=', rec.id)])

    def _compute_pr_count(self):
        for rec in self:
            rec.pr_count = self.env['purchase.request'].search_count([('store_request_id', '=', rec.id)])

    def pr_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Request',
            'res_model': 'purchase.request',
            'domain': [('store_request_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

    def siv_action(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'store issue',
            'res_model': 'store.issue.voucher',
            'domain': [('request_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

    def action_submit(self):
        if any(line.quantity <= 0 for line in self.request_lines):
            raise ValidationError("Product Quantity to request can not be empty")
        self.state = 'to_approve'
        # self.checked_by = self.env.user
        # self.checked_date = fields.Date.today()

    def action_approve(self):
        self.state = 'approved'
        self.approved_by = self.env.user
        self.approved_date = fields.Date.today()

    def action_reject(self):
        self.state = 'reject'

    def create_purchase_request(self):
        self.ensure_one()
        wizard = self.env['store.request.purchase.wizard'].create({
            'store_request_id': self.id,
            'line_ids': [(0, 0, {
                'product_id': line.product_id.id,
                'requested_quantity': line.quantity,
                'available_quantity': line.qty_available,
                'quantity_to_purchase': max(0, line.quantity - line.qty_available)
            }) for line in self.request_lines if line.quantity > line.qty_available and not line.fulfilled]
        })
        
        return {
            'name': _('Create Purchase Request'),
            'type': 'ir.actions.act_window',
            'res_model': 'store.request.purchase.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def create_issue_voucher(self):
        self.ensure_one()
        wizard = self.env['store.request.siv.wizard'].create({
            'store_request_id': self.id,
            'line_ids': [(0, 0, {
                'product_id': line.product_id.id,
                'requested_quantity': line.quantity,
                'available_quantity': line.qty_available,
                'quantity_to_issue': min(line.quantity, line.qty_available)
            }) for line in self.request_lines if line.qty_available >= line.quantity and not line.fulfilled]
        })
        
        return {
            'name': _('Create Store Issue Voucher'),
            'type': 'ir.actions.act_window',
            'res_model': 'store.request.siv.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def create_issue_and_voucher(self):
        self.create_issue_voucher()
        self.create_purchase_request()

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('store.request') or _('New')
            res = super(StoreRequest, self).create(vals)
            return res
    @api.constrains('request_lines')
    def _check_request_lines(self):
        for record in self:
            if not record.request_lines:
                raise ValidationError("At least one line is required in Request Lines.")
class StoreRequestLine(models.Model):
    _name = 'store.request.line'
    _description = 'Store Request Line'

    sequence = fields.Integer(string='SN', default="10")

    request_id = fields.Many2one('store.request', string='Store Request')
    product_id = fields.Many2one('product.product', string='Product/Description', required=True, )
    quantity = fields.Float(string='Quantity', required=True, default=1.00)
    qty_available = fields.Float( string="On-Hand Quantity", related='product_id.qty_available', readonly=True )
    # unit_price = fields.Float(string="Unit Price", default=False, required=True) 
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure", related= "product_id.uom_po_id")
    remark = fields.Char(string="Remark")
    fulfilled= fields.Boolean(default=False)

    _order = 'request_id, sequence'

    @api.model
    def create(self, values):
        if 'sequence' not in values:
            values['sequence'] = self._get_last_sequence(values.get('request_id')) + 1
        return super(StoreRequestLine, self).create(values)

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