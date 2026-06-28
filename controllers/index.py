from odoo import http
from odoo.http import request
from odoo.tools.image import image_data_uri


class TimeAccessPortal(http.Controller):
    @http.route('/index', type='http', auth='user', website=True)
    def index_f(self, sort='default', category_id=None, **kw):

        domain = [
            ('is_b2b_portal', '=', True)
        ]

        selected_category_id = False

        # Category filter
        if category_id and str(category_id).isdigit():
            selected_category_id = int(category_id)
            domain.append(('categ_id', 'child_of', selected_category_id))

        # product sort desc and asc
        order = 'id desc'
        if sort == 'low-high':
            order = 'list_price asc'
        elif sort == 'high-low':
            order = 'list_price desc'

        products = request.env['product.template'].sudo().search(domain, order=order)
        # Only categories used by B2B portal products
        b2b_products = request.env['product.template'].sudo().search([
            ('is_b2b_portal', '=', True),
            ('categ_id', '!=', False),
        ])
        categories = b2b_products.mapped('categ_id')

        return request.render('time_access_portal.index_page', {
            'active_menu': 'products',
            'products': products,
            'sort': sort,
            'b2b_products': b2b_products,
            'categories': categories,
            'selected_category_id':selected_category_id
        })
