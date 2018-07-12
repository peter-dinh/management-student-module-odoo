# -*- coding: utf-8 -*-
{
    'name': "Management students",

    'summary': """
        Its basic module""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Peter Dinh",
    'website': "https://peterdinh.tk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'student',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/view_report.xml',
        'security/qlsv_security.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}