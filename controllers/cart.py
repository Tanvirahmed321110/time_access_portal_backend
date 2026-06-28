from odoo import http
from odoo.http import request

class TimeAccessPortal(http.Controller):

    # ==================  Cart  Page ===================
    @http.route('/cart', type='http', auth='user', website=True)
    def index_f(self, **kw):

        partner = request.env.user.partner_id

        order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'draft')
        ],limit=1)

        order_lines = order.order_line if order else []

        return request.render('time_access_portal.cart_page', {
            'order': order,
            'order_lines': order_lines,
        })


    # ==================  Add To Cart  ===================
    @http.route('/cart/add', type='json', auth='user', website=True)
    def add_to_cart(self, product_id, quantity=1, **kw):
        partner = request.env.user.partner_id

        # Existing draft order  check
        order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'draft'),
        ], limit=1)

        #  draft order
        if not order:
            order = request.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'state': 'draft',
            })

        # Product check
        existing_line = order.order_line.filtered(
            lambda l: l.product_id.id == product_id
        )

        if existing_line:
            existing_line.product_uom_qty += quantity
        else:
            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'product_id': product_id,
                'product_uom_qty': quantity,
            })

        return {'success': True, 'order_id': order.id}



    # ==================  Cart  Remove  ===================
    @http.route('/cart/remove', type='json', auth='user', website=True)
    def remove_from_cart(self, line_id, **kw):
        line = request.env['sale.order.line'].sudo().search([
            ('id', '=', line_id),
            ('order_id.partner_id', '=', request.env.user.partner_id.id),
            ('order_id.state', '=', 'draft'),
        ], limit=1)

        if line:
            line.unlink()
            return {'success': True}
        return {'success': False}

