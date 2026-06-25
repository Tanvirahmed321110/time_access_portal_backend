from odoo import http
from odoo.http import request
from odoo.tools.image import image_data_uri


class TimeAccessPortal(http.Controller):
    @http.route('/index', type='http', auth='user', website=True)

    def index_f(self, **kw):

        products = request.env['product.template'].sudo().search([
            ('is_b2b_portal', '=', True)
        ])


        return request.render('time_access_portal.index_page', {
            'active_menu': 'products',
            'products':products,
        })

