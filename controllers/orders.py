from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    # ===================  Orders Page  ====================
    @http.route('/orders', type='http', auth='user', website=True)
    def index_f(self, **kw):
        return request.render('time_access_portal.orders_page', {
            'active_menu': 'orders',
        })


    # ===================  Orders Details Page  ====================
    @http.route('/orders/order-details', type='http', auth='user', website=True)
    def order_details_f(self, **kw):
        return request.render('time_access_portal.order_details_page', {
            'active_menu': 'orders',
        })

