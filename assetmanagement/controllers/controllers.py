# -*- coding: utf-8 -*-
# from odoo import http


# class Assetmanagement(http.Controller):
#     @http.route('/assetmanagement/assetmanagement', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/assetmanagement/assetmanagement/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('assetmanagement.listing', {
#             'root': '/assetmanagement/assetmanagement',
#             'objects': http.request.env['assetmanagement.assetmanagement'].search([]),
#         })

#     @http.route('/assetmanagement/assetmanagement/objects/<model("assetmanagement.assetmanagement"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('assetmanagement.object', {
#             'object': obj
#         })

