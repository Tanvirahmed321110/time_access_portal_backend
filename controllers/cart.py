from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):


    # ================== Cart Page ===================
    @http.route('/cart', type='http', auth='user', website=True)
    def index_f(self, **kw):
        # Block B2B General User from /index portal
        if (
                request.env.user.has_group('time_access_portal.group_b2b_general_user')
                and not request.env.user.has_group('time_access_portal.group_b2b_management')
        ):
            return request.redirect('/web')

        partner = request.env.user.partner_id

        order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'add_to_cart'),
        ], limit=1)

        order_lines = order.order_line if order else []

        # =====================================================
        # B2B Minimum Qty Logic
        # Product b2b_qty first.
        # If product b2b_qty empty/0, then category b2b_quantity.
        # If both empty/0, fallback 1.
        # =====================================================
        product_min_qty_map = {}
        product_stock_qty_map = {}
        product_default_qty_map = {}

        for product in products:
            variant = product.product_variant_id

            stock_qty = int(variant.qty_available or 0)

            product_min_qty = int(product.b2b_qty or 0)
            category_min_qty = int(product.categ_id.b2b_quantity or 0)

            min_qty = product_min_qty or category_min_qty or 1

            if stock_qty >= min_qty:
                default_qty = min_qty
            else:
                default_qty = stock_qty

            product_min_qty_map[product.id] = min_qty
            product_stock_qty_map[product.id] = stock_qty
            product_default_qty_map[product.id] = default_qty

        return request.render('time_access_portal.cart_page', {
            'order': order,
            'order_lines': order_lines,
        })

    # ================== Add To Cart ===================
    @http.route('/cart/add', type='json', auth='user', website=True)
    def add_to_cart(self, product_id, quantity=1, replace_qty=False, **kw):
        partner = request.env.user.partner_id

        product = request.env['product.product'].sudo().browse(int(product_id)).exists()
        if not product:
            return {
                'success': False,
                'message': 'Product not found',
            }

        quantity = float(quantity or 1)

        if quantity < 1:
            quantity = 1

        # Convert JS true/false safely
        replace_qty = bool(replace_qty)

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
            line = existing_line[0]

            new_qty = quantity

            line.sudo().write({
                'product_uom_qty': new_qty,
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