# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseManagement(http.Controller):
#     @http.route('/purchase_management/purchase_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_management/purchase_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_management.listing', {
#             'root': '/purchase_management/purchase_management',
#             'objects': http.request.env['purchase_management.purchase_management'].search([]),
#         })

#     @http.route('/purchase_management/purchase_management/objects/<model("purchase_management.purchase_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_management.object', {
#             'object': obj
#         })

