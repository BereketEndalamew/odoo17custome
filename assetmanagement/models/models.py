from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from collections import defaultdict
from datetime import date
import logging

_logger = logging.getLogger(__name__)
class AssetAssignment(models.Model):
    _name = 'asset.assignment'
    _description = 'Asset Assignment'

    asset_name = fields.Many2one('hr.employee', string="Asset Name", required=True)
    serial_number = fields.Char(string="Serial Number", required=True)
    description = fields.Text(string="Description")
    product_id = fields.Many2one('product.product', string="Asset Product", required=True)
    employee_id = fields.Many2one('hr.employee', string="Assigned Employee", required=True)
    assignment_date = fields.Date(string="Assignment Date", default=fields.Date.today, required=True)
    state = fields.Selection([
        ('assigned', 'Assigned'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ], default='assigned', string='Status')

    # Optionally, you can add a return date field if necessary
    return_date = fields.Date(string="Return Date")
    is_overdue = fields.Boolean(string="Is Overdue", compute='_compute_is_overdue')
    current_state = fields.Char(string="Current State", compute='_compute_current_state')

    assigned_count = fields.Integer(string="Assigned", compute='_compute_state_counts1')
    returned_count = fields.Integer(string="Returned", compute='_compute_state_counts2')
    overdue_count = fields.Integer(string="Overdue", compute='_compute_state_counts3')

    @api.depends('state', 'return_date')
    def _compute_current_state(self):
        today = date.today()
        for record in self:
            if record.state == 'assigned' and record.return_date:
                if record.return_date < today:
                    record.current_state = 'Overdue'
                else:
                    record.current_state = 'Assigned'
            elif record.state == 'returned':
                record.current_state = 'Returned'
            else:
                record.current_state = 'Unknown'

    @api.depends('return_date', 'state')
    def _compute_is_overdue(self):
        today = date.today()
        for record in self:
            record.is_overdue = (
                    record.state == 'assigned' and
                    record.return_date and
                    record.return_date < today
            )
        # Button: Mark as Overdue

    def action_mark_overdue(self):
        for record in self:
            if record.state == 'assigned' and record.return_date and record.return_date < date.today():
                record.state = 'overdue'

    # Compute or Onchange logic for serial number or any other rules can be added here
    @api.constrains('assignment_date', 'return_date')
    def _check_dates(self):
        for record in self:
            today = date.today()

            # Check: assignment date cannot be in the future
            if record.assignment_date and record.assignment_date > today:
                raise ValidationError("Assignment date cannot be in the future.")

            # Check: return date cannot be before assignment date
            if record.return_date and record.return_date < record.assignment_date:
                raise ValidationError("Return date cannot be earlier than assignment date.")

    # 🔘 Button: Request Return
    def action_request_return(self):
        for record in self:
            record.write({
                'state': 'assigned'
            })
            record.action_verify_return()

    # 🔘 Button: Verify Return
    def action_verify_return(self):
        for record in self:
            # Check if the return date or return deadline is in the future
            if record.return_date and record.return_date > fields.Date.today():
                raise UserError("The return date is in the future, so the asset cannot be returned yet.")
            record.write({
                'state': 'returned'
            })
            _logger.info(f"Asset {record.asset_name.name} has been returned.")

    @api.model
    def cron_update_asset_status(self):
        today = date.today()

        # Find assets where return date is set
        assigned_records = self.search([('state', '=', 'assigned'), ('return_date', '!=', False)])

        for record in assigned_records:
            if record.return_date and record.return_date < today:
                if record.state != 'returned':  # If already returned, no need to update
                    record.state = 'overdue'  # Set status to overdue if not returned
                    _logger.info("***Overdue***")
                    _logger.info("Asset Overdue:Asset: %s | Assigned: %s | Return: %s",
                                 record.asset_name,
                                 record.assignment_date,
                                 record.return_date)


        # Find all assets that are marked as returned, and set their state to 'returned'
        returned_records = self.search([('state', '=', 'assigned'), ('return_date', '!=', False)])

        for record in returned_records:
            if record.return_date and record.return_date < today:
                record.state = 'returned'  # Mark it as returned if it's passed its return date
                _logger.info("***Returned***")
                _logger.info("Asset Returned:Asset: %s | Assigned: %s | Return: %s",
                             record.asset_name,
                             record.assignment_date,
                             record.return_date)
        # Method to group records by state dynamically

    @api.depends()
    def _compute_state_counts1(self):
        for record in self:
            record.assigned_count = self.env['asset.assignment'].search_count([('state', '=', 'assigned')])

    @api.depends()
    def _compute_state_counts2(self):
        for record in self:
            record.returned_count = self.env['asset.assignment'].search_count([('state', '=', 'returned')])

    @api.depends()
    def _compute_state_counts3(self):
        for record in self:
            record.overdue_count = self.env['asset.assignment'].search_count([('state', '=', 'overdue')])

    def action_show_assigned(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assigned Assets',
            'res_model': 'asset.assignment',
            'view_mode': 'tree,form',
            'domain': [('state', '=', 'assigned')],
            'target':'new',
        }

    def action_show_returned(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Returned Assets',
            'res_model': 'asset.assignment',
            'view_mode': 'tree,form',
            'domain': [('state', '=', 'returned')],
            'target': 'new',

        }

    def action_show_overdue(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Overdue Assets',
            'res_model': 'asset.assignment',
            'view_mode': 'tree,form',
            'domain': [('state', '=', 'overdue')],
            'target': 'new',

        }
