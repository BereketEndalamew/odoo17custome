from odoo import api, models, fields

class RequestApprovalLine(models.Model):
    _name = "request.approval.line"
    _description = "Approval History"

    request_id = fields.Many2one('request.approval', string="Request", required=True, ondelete='cascade')
    approver_id = fields.Many2one('res.users', string="Approver")
    date_action = fields.Datetime(string="Action Date", default=fields.Datetime.now)
    action = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Action", required=True)
    comments = fields.Text(string="Comments")

    def action_approve_request(self):
        """Approve the related request and log the action."""
        if self.request_id:
            self.request_id.state1 = 'approved'
            self.create({
                'request_id': self.request_id.id,
                'approver_id': self.env.user.id,
                'action': 'approved',
                'comments': 'Approved by ' + self.env.user.name
            })

    def action_reject_request(self):
        """Reject the related request and log the action."""
        if self.request_id:
            self.request_id.state1 = 'rejected'
            self.create({
                'request_id': self.request_id.id,
                'approver_id': self.env.user.id,
                'action': 'rejected',
                'comments': 'Rejected by ' + self.env.user.name
            })
