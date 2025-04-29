# -*- coding: utf-8 -*-
# from odoo import http


# class Dashboard(http.Controller):
#     @http.route('/dashboard/dashboard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dashboard/dashboard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dashboard.listing', {
#             'root': '/dashboard/dashboard',
#             'objects': http.request.env['dashboard.dashboard'].search([]),
#         })

#     @http.route('/dashboard/dashboard/objects/<model("dashboard.dashboard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dashboard.object', {
#             'object': obj
#         })

