# -*- coding: utf-8 -*-
# from odoo import http


# class FilterRemoval(http.Controller):
#     @http.route('/filter_removal/filter_removal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/filter_removal/filter_removal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('filter_removal.listing', {
#             'root': '/filter_removal/filter_removal',
#             'objects': http.request.env['filter_removal.filter_removal'].search([]),
#         })

#     @http.route('/filter_removal/filter_removal/objects/<model("filter_removal.filter_removal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('filter_removal.object', {
#             'object': obj
#         })

