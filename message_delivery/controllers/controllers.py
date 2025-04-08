# -*- coding: utf-8 -*-
# from odoo import http


# class MessageDelivery(http.Controller):
#     @http.route('/message_delivery/message_delivery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/message_delivery/message_delivery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('message_delivery.listing', {
#             'root': '/message_delivery/message_delivery',
#             'objects': http.request.env['message_delivery.message_delivery'].search([]),
#         })

#     @http.route('/message_delivery/message_delivery/objects/<model("message_delivery.message_delivery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('message_delivery.object', {
#             'object': obj
#         })

