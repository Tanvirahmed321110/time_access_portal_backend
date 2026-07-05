from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):


    # ================== Cart Page ===================
    @http.route('/cart', type='http', auth='user', website=True)
    def index_f(self, **kw):
        partner = request.env.user.partner_id

        order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'add_to_cart'),
        ], limit=1)

        order_lines = order.order_line if order else []

        return request.render('time_access_portal.cart_page', {
            'order': order,
            'order_lines': order_lines,
        })

    # ================== Add To Cart ===================
    @http.route('/cart/add', type='json', auth='user', website=True)
    def add_to_cart(self, product_id, quantity=1, **kw):
        partner = request.env.user.partner_id

        product = request.env['product.product'].sudo().browse(int(product_id)).exists()
        if not product:
            return {
                'success': False,
                'message': 'Product not found',
            }

        quantity = float(quantity or 1)

        order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'add_to_cart'),
        ], limit=1)

        if not order:
            order = request.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'state': 'add_to_cart',
            })

        existing_line = order.order_line.filtered(
            lambda line: line.product_id.id == product.id
        )

        if existing_line:
            existing_line[0].sudo().write({
                'product_uom_qty': existing_line[0].product_uom_qty + quantity,
            })
        else:
            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'product_id': product.id,
                'product_uom_qty': quantity,
                'product_uom': product.uom_id.id,
            })

        return {
            'success': True,
            'order_id': order.id,
        }

    # ================== Cart Remove ===================
    @http.route('/cart/remove', type='json', auth='user', website=True)
    def remove_from_cart(self, line_id, **kw):
        line = request.env['sale.order.line'].sudo().search([
            ('id', '=', int(line_id)),
            ('order_id.partner_id', '=', request.env.user.partner_id.id),
            ('order_id.state', '=', 'add_to_cart'),
        ], limit=1)

        if line:
            order = line.order_id
            line.unlink()

            return {
                'success': True,
                'amount_untaxed': float(order.amount_untaxed),
                'amount_tax': float(order.amount_tax),
                'amount_total': float(order.amount_total),
            }

        return {'success': False}

    # ================== Update Quantity ===================
    @http.route('/cart/update_qty', type='json', auth='user', website=True)
    def update_cart_qty(self, line_id, quantity, **kw):
        line = request.env['sale.order.line'].sudo().search([
            ('id', '=', int(line_id)),
            ('order_id.partner_id', '=', request.env.user.partner_id.id),
            ('order_id.state', '=', 'add_to_cart'),
        ], limit=1)

        if line:
            order = line.order_id
            quantity = float(quantity or 1)

            if quantity < 1:
                quantity = 1

            line.sudo().write({
                'product_uom_qty': quantity,
            })

            return {
                'success': True,
                'amount_untaxed': float(order.amount_untaxed),
                'amount_tax': float(order.amount_tax),
                'amount_total': float(order.amount_total),
                'price_subtotal': float(line.price_subtotal),
            }

        return {'success': False}