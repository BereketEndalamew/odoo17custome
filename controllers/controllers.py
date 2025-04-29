# -*- coding: utf-8 -*-
# from odoo import http


# class EmailNotification(http.Controller):
#     @http.route('/email_notification/email_notification', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/email_notification/email_notification/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('email_notification.listing', {
#             'root': '/email_notification/email_notification',
#             'objects': http.request.env['email_notification.email_notification'].search([]),
#         })

#     @http.route('/email_notification/email_notification/objects/<model("email_notification.email_notification"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('email_notification.object', {
#             'object': obj
#         })

