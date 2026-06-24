from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    @http.route('/index/cart/checkout/order_invoice', type='http', auth='user', website=True)
    def invoice_f(self, **kw):
        return request.render('time_access_portal.order_invoice_page', {
            '': '',
        })

