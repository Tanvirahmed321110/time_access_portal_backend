# -*- coding: utf-8 -*-
{
    'name': "Time Access",

    'summary': """
         WholeSeller Portal """,

    'description': """
        Time Access whole seller portal
    """,

    'author': "Tanvir Ahmed",
    'website': "http://www.xsellencebdltd.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'templates/layout.xml',
        'templates/index.xml',
        'templates/cart.xml',
        'templates/checkout.xml',
        'templates/profile.xml',
        'templates/orders.xml',
        'templates/order_details.xml',
        'templates/pagination.xml',


        # views
        'views/product_product_view.xml',
        'views/sequence_inherit.xml',
        'views/category_inherit.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # 'time_access_portal/static/src/css/custom_class.css',
        ],

        'web.assets_backend': [
            'time_access_portal/static/src/css/custom_backend.css',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}