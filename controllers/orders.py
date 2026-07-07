from odoo import http
from odoo.http import request
from odoo.addons.time_access_portal.utilitis.pagination import get_pager


class TimeAccessPortal(http.Controller):

    # ===================  Orders Page  ====================
    @http.route('/orders', type='http', auth='user', website=True)
    def index_f(self, **kw):
        # Block B2B General User from /index portal
        if (
                request.env.user.has_group('time_access_portal.group_b2b_general_user')
                and not request.env.user.has_group('time_access_portal.group_b2b_management')
        ):
            return request.redirect('/web')

        partner = request.env.user.partner_id

        domain = [
            ('partner_id', '=', partner.id),
            ('state', 'in', ['sale', 'done', 'cancel','draft']),
        ]

        # ===== Pagination Setup =====
        per_page = int(kw.get('per_page', 15))
        total = request.env['sale.order'].sudo().search_count(domain)

        pager = get_pager(
            url='/orders',
            total=total,
            page=kw.get('page', 1),
            per_page=per_page,
        )

        orders = request.env['sale.order'].sudo().search(
            domain,
            order='id desc',
            offset=pager['offset'],
            limit=pager['per_page']
        )

        return request.render('time_access_portal.orders_page', {
            'active_menu': 'orders',
            'orders': orders,
            'pager': pager,
            'total': total,
        })


    # ===================  Orders Details Page  ====================
    @http.route('/orders/<int:order_id>', type='http', auth='user', website=True)
    def order_details_f(self, order_id, **kw):
        # Block B2B General User from /index portal
        if (
                request.env.user.has_group('time_access_portal.group_b2b_general_user')
                and not request.env.user.has_group('time_access_portal.group_b2b_management')
        ):
            return request.redirect('/web')

        partner = request.env.user.partner_id

        order = request.env['sale.order'].sudo().search([
            ('id', '=', order_id),
            ('partner_id', '=', partner.id),
        ])

        delivery_date = None
        if order:
            picking = request.env['stock.picking'].sudo().search([
                ('sale_id', '=', order.id),
                ('state', '=', 'done')
            ], limit=1, order='date_done desc')

            if picking and picking.date_done:
                delivery_date = picking.date_done

        return request.render('time_access_portal.order_details_page', {
            'active_menu': 'orders',
            'order': order,
            'order_lines': order.order_line if order else [],
            'delivery_date': delivery_date
        })