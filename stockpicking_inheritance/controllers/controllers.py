# -*- coding: utf-8 -*-
# from odoo import http


# class StockpickingInheritance(http.Controller):
#     @http.route('/stockpicking_inheritance/stockpicking_inheritance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stockpicking_inheritance/stockpicking_inheritance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stockpicking_inheritance.listing', {
#             'root': '/stockpicking_inheritance/stockpicking_inheritance',
#             'objects': http.request.env['stockpicking_inheritance.stockpicking_inheritance'].search([]),
#         })

#     @http.route('/stockpicking_inheritance/stockpicking_inheritance/objects/<model("stockpicking_inheritance.stockpicking_inheritance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stockpicking_inheritance.object', {
#             'object': obj
#         })

