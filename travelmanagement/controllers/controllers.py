# -*- coding: utf-8 -*-
# from odoo import http


# class Travelmanagement(http.Controller):
#     @http.route('/travelmanagement/travelmanagement', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travelmanagement/travelmanagement/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('travelmanagement.listing', {
#             'root': '/travelmanagement/travelmanagement',
#             'objects': http.request.env['travelmanagement.travelmanagement'].search([]),
#         })

#     @http.route('/travelmanagement/travelmanagement/objects/<model("travelmanagement.travelmanagement"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travelmanagement.object', {
#             'object': obj
#         })

