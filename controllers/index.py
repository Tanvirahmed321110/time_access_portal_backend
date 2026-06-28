from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    @http.route('/index', type='http', auth='user', website=True)
    def index_f(self, sort='default', category_id=None, **kw):

        domain = [
            ('is_b2b_portal', '=', True)
        ]

        selected_category_id = False

        # Only checked B2B categories will show in UI
        categories = request.env['product.category'].sudo().search([
            ('is_b2b_category', '=', True)
        ])

        # Category filter
        if category_id and str(category_id).isdigit():
            category = request.env['product.category'].sudo().search([
                ('id', '=', int(category_id)),
                ('is_b2b_category', '=', True),
            ], limit=1)

            if category:
                selected_category_id = category.id
                domain.append(('categ_id', 'child_of', selected_category_id))

        #=======  Product sort desc and asc  =========
        order = 'id desc'

        if sort == 'low-high':
            order = 'list_price asc'
        elif sort == 'high-low':
            order = 'list_price desc'

        products = request.env['product.template'].sudo().search(domain, order=order)

        return request.render('time_access_portal.index_page', {
            'active_menu': 'products',
            'products': products,
            'sort': sort,
            'categories': categories,
            'selected_category_id': selected_category_id,
        })