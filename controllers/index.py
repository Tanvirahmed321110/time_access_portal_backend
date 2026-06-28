from odoo import http
from odoo.http import request
from odoo.tools.image import image_data_uri


class TimeAccessPortal(http.Controller):
    @http.route('/index', type='http', auth='user', website=True)

    def index_f(self,sort='default', **kw):

        domain = [
            ('is_b2b_portal', '=', True)
        ]

        #product sort desc and asc
        order = 'id desc'
        if sort == 'low-high':
            order = 'list_price asc'
        elif sort == 'high-low':
            order = 'list_price desc'

        products = request.env['product.template'].sudo().search(domain,order=order)

        return request.render('time_access_portal.index_page', {
            'active_menu': 'products',
            'products':products,
            'sort':sort,
        })

