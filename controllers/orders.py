from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    # ===================  Orders Page  ====================
    @http.route('/orders', type='http', auth='user', website=True)
    def index_f(self, **kw):
        partner = request.env.user.partner_id

        orders = request.env['sale.order'].sudo().search([
            ('partner_id','=', partner.id),
            ('state', 'in', ['sale','done','cancel']),
        ],order='id desc')

        return request.render('time_access_portal.orders_page', {
            'active_menu': 'orders',
            'orders' : orders
        })


    # ===================  Orders Details Page  ====================
    @http.route('/orders/<int:order_id>', type='http', auth='user', website=True)
    def order_details_f(self,order_id ,**kw ):
        partner = request.env.user.partner_id

        order = request.env['sale.order'].sudo().search([
            ('id','=', order_id),
            ('partner_id','=', partner.id),
        ])

        return request.render('time_access_portal.order_details_page', {
            'active_menu': 'orders',
            'order': order,
            'order_lines': order.order_line if order else [],
        })

