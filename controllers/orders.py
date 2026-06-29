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

        # delivery date
        delivery_date = None
        if order:
            # এই সেলস অর্ডারের আন্ডারে যে ডেলিভারি চালানগুলো (Pickings) আছে তা খোঁজা হচ্ছে
            picking = request.env['stock.picking'].sudo().search([
                ('sale_id', '=', order.id),
                ('state', '=', 'done')  # শুধুমাত্র সফলভাবে ডেলিভারি হওয়া চালান
            ], limit=1, order='date_done desc')

            if picking and picking.date_done:
                delivery_date = picking.date_done

        return request.render('time_access_portal.order_details_page', {
            'active_menu': 'orders',
            'order': order,
            'order_lines': order.order_line if order else [],
            'delivery_date':delivery_date
        })

