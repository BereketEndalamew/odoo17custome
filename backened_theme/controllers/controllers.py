# -*- coding: utf-8 -*-
# from odoo import http


# class BackenedTheme(http.Controller):
#     @http.route('/backened_theme/backened_theme', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/backened_theme/backened_theme/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('backened_theme.listing', {
#             'root': '/backened_theme/backened_theme',
#             'objects': http.request.env['backened_theme.backened_theme'].search([]),
#         })

#     @http.route('/backened_theme/backened_theme/objects/<model("backened_theme.backened_theme"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('backened_theme.object', {
#             'object': obj
#         })

