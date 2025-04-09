# -*- coding: utf-8 -*-
# from odoo import http


# class Evantrading(http.Controller):
#     @http.route('/evantrading/evantrading', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/evantrading/evantrading/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('evantrading.listing', {
#             'root': '/evantrading/evantrading',
#             'objects': http.request.env['evantrading.evantrading'].search([]),
#         })

#     @http.route('/evantrading/evantrading/objects/<model("evantrading.evantrading"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('evantrading.object', {
#             'object': obj
#         })

