# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryManagement(http.Controller):
#     @http.route('/inventory_management/inventory_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_management/inventory_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_management.listing', {
#             'root': '/inventory_management/inventory_management',
#             'objects': http.request.env['inventory_management.inventory_management'].search([]),
#         })

#     @http.route('/inventory_management/inventory_management/objects/<model("inventory_management.inventory_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_management.object', {
#             'object': obj
#         })

