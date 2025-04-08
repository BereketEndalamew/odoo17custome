# -*- coding: utf-8 -*-
{
    'name': "hospitalsystem",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/patient_view.xml',
        'views/appointement_view.xml',
        'views/menu.xml',
        'wizard/travel_booking.xml',
        'views/views.xml',
        'data/ir_crone.xml',
        'report/report_template.xml',
        'report/sale_order_report.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

