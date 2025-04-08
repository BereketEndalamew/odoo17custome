# -*- coding: utf-8 -*-
# from odoo import http


# class Travelbooking(http.Controller):
#     @http.route('/travelbooking/travelbooking', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travelbooking/travelbooking/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('travelbooking.listing', {
#             'root': '/travelbooking/travelbooking',
#             'objects': http.request.env['travelbooking.travelbooking'].search([]),
#         })

#     @http.route('/travelbooking/travelbooking/objects/<model("travelbooking.travelbooking"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travelbooking.object', {
#             'object': obj
#         })

