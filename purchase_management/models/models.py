# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class purchase_management(models.Model):
#     _name = 'purchase_management.purchase_management'
#     _description = 'purchase_management.purchase_management'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

