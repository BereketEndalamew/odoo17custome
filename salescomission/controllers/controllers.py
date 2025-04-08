# -*- coding: utf-8 -*-
# from odoo import http


# class Salescomission(http.Controller):
#     @http.route('/salescomission/salescomission', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salescomission/salescomission/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('salescomission.listing', {
#             'root': '/salescomission/salescomission',
#             'objects': http.request.env['salescomission.salescomission'].search([]),
#         })

#     @http.route('/salescomission/salescomission/objects/<model("salescomission.salescomission"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salescomission.object', {
#             'object': obj
#         })

