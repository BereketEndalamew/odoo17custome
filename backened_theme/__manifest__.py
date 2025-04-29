{
    'name': 'Theme Customization',
    'version': '1.0',
    'summary': 'Customize theme colors and branding',
    'description': 'Allows customization of theme colors, logos, and favicons',
    'author': 'Your Name',
    'depends': ['base','web'],
    'data': [
        'views/res_config_settings_views.xml',
        'static/xml/theme_customization_templates.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'your_module/static/src/scss/theme_options.scss',
    #     ],
    # },
    'installable': True,
    'application': False,
}