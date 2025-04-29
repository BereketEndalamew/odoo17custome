# -*- coding: utf-8 -*-
# from odoo import http


# class FinanceAccounting(http.Controller):
#     @http.route('/finance_accounting/finance_accounting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/finance_accounting/finance_accounting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('finance_accounting.listing', {
#             'root': '/finance_accounting/finance_accounting',
#             'objects': http.request.env['finance_accounting.finance_accounting'].search([]),
#         })

#     @http.route('/finance_accounting/finance_accounting/objects/<model("finance_accounting.finance_accounting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('finance_accounting.object', {
#             'object': obj
#         })

