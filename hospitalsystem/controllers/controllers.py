# -*- coding: utf-8 -*-
# from odoo import http


# class Hospitalsystem(http.Controller):
#     @http.route('/hospitalsystem/hospitalsystem', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hospitalsystem/hospitalsystem/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hospitalsystem.listing', {
#             'root': '/hospitalsystem/hospitalsystem',
#             'objects': http.request.env['hospitalsystem.hospitalsystem'].search([]),
#         })

#     @http.route('/hospitalsystem/hospitalsystem/objects/<model("hospitalsystem.hospitalsystem"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hospitalsystem.object', {
#             'object': obj
#         })

