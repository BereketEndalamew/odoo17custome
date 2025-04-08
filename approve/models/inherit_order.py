from odoo import api, fields, models

class Inherit(models.Model):
    _inherit='sale.order'

    appointement_date=fields.Date('Appointment Date')