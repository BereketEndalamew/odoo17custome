from odoo import http
from odoo.http import request


class HospitalDashboardController(http.Controller):

    @http.route('/ho spital/dashboard', auth='user', type='json')
    def get_appointment_stats(self):
        model = request.env['hospital.appointement']
        return {"models":model}
        return request.render("hospitalsystem",{
            'models':model
            # 'draft_count': model.search_count([('state1', '=', 'draft')]),
            # 'done_count': model.search_count([('state1', '=', 'done')]),
            # 'in_consultation_count': model.search_count([('state1', '=', 'in_consultation')]),
            # 'cancel_count': model.search_count([('state1', '=', 'cancel')]),
        })
