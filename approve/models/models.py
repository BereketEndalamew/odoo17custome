from odoo import models, fields, api

class RequestApproval(models.Model):
    _name = "request.approval"
    _description = "Request Approval System"

    name = fields.Char(string="Request Title", required=True)
    description = fields.Text(string="Description")
    requester_id = fields.Many2one('res.users', string="Requester", default=lambda self: self.env.user, readonly=True)
    approver_id = fields.Many2one('res.users', string="Approver")
    date_requested = fields.Datetime(string="Requested Date", default=fields.Datetime.now, readonly=True)

    state1 = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default='draft')

    approval_lines = fields.One2many('request.approval.line', 'request_id', string="Approval History", readonly=True)

    def action_submit(self):
        """Submit the request for approval."""
        self.state1 = 'submitted'

    def action_set_draft(self):
        """Move back to draft (if needed)."""
        self.state1 = 'draft'
