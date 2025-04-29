from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    brand_color = fields.Char(string="Brand", default="#28a745")
    primary_color = fields.Char(string="Primary", default="#28a745")
    menu_text_color = fields.Char(string="Menu Text", default="#000000")
    apps_text_color = fields.Char(string="Apps Text", default="#000000")
    apps_active_color = fields.Char(string="Apps Active", default="#28a745")
    background_color = fields.Char(string="Background", default="#e0e0e0")

    info_color = fields.Char(string="Info", default="#17a2b8")
    success_color = fields.Char(string="Success", default="#28a745")
    warning_color = fields.Char(string="Warning", default="#ffc107")
    danger_color = fields.Char(string="Danger", default="#dc3545")

    background_image = fields.Binary(string="Background Image")
    background_image_filename = fields.Char()

    logo = fields.Binary(string="Logo")
    logo_filename = fields.Char()
