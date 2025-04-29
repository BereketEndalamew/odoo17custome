# -*- coding: utf-8 -*-
# from odoo import http


# class SalesManagement(http.Controller):
#     @http.route('/sales_management/sales_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_management/sales_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_management.listing', {
#             'root': '/sales_management/sales_management',
#             'objects': http.request.env['sales_management.sales_management'].search([]),
#         })

#     @http.route('/sales_management/sales_management/objects/<model("sales_management.sales_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_management.object', {
#             'object': obj
#         })

