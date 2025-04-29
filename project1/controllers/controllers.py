# -*- coding: utf-8 -*-
# from odoo import http


# class Project1(http.Controller):
#     @http.route('/project1/project1', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project1/project1/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project1.listing', {
#             'root': '/project1/project1',
#             'objects': http.request.env['project1.project1'].search([]),
#         })

#     @http.route('/project1/project1/objects/<model("project1.project1"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project1.object', {
#             'object': obj
#         })

