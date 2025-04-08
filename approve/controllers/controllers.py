# -*- coding: utf-8 -*-
# from odoo import http


# class Approve(http.Controller):
#     @http.route('/approve/approve', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/approve/approve/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('approve.listing', {
#             'root': '/approve/approve',
#             'objects': http.request.env['approve.approve'].search([]),
#         })

#     @http.route('/approve/approve/objects/<model("approve.approve"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('approve.object', {
#             'object': obj
#         })

