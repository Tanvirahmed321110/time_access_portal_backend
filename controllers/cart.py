from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    @http.route('/index/cart', type='http', auth='user', website=True)
    def index_f(self, **kw):
        return request.render('time_access_portal.cart_page', {
            '': '',
        })

