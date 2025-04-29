from odoo import models

class StockPickingReport(models.Model):
    _inherit = 'ir.actions.report'

    def _get_report_values(self, docids, data=None):
        # Override this function if additional context or data is needed
        return super(StockPickingReport, self)._get_report_values(docids, data)
