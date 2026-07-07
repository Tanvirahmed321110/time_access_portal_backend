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
        line_min_qty_map = {}
        line_stock_qty_map = {}

        for line in order_lines:
            product = line.product_id
            product_tmpl = product.product_tmpl_id

            stock_qty = int(product.qty_available or 0)

            product_min_qty = int(product_tmpl.b2b_qty or 0)
            category_min_qty = int(product_tmpl.categ_id.b2b_quantity or 0)

            min_qty = product_min_qty or category_min_qty or 1

            line_min_qty_map[line.id] = min_qty
            line_stock_qty_map[line.id] = stock_qty

        return request.render('time_access_portal.cart_page', {
            'order': order,
            'order_lines': order_lines,
            'line_min_qty_map': line_min_qty_map,
            'line_stock_qty_map': line_stock_qty_map,
        })



    # ================== Add To Cart ===================
    # ================== Add To Cart ===================
    @http.route('/cart/add', type='json', auth='user', website=True)
    def add_to_cart(self, product_id, quantity=1, replace_qty=False, **kw):
        partner = request.env.user.partner_id

        Product = request.env['product.product'].sudo()
        SaleOrder = request.env['sale.order'].sudo()
        SaleOrderLine = request.env['sale.order.line'].sudo()

        product = Product.browse(int(product_id)).exists()
        if not product:
            return {
                'success': False,
                'message': 'Product not found',
            }

        quantity = float(quantity or 1)
        if quantity < 1:
            quantity = 1

        replace_qty = bool(replace_qty)

        has_b2b_sale = 'b2b_sale' in SaleOrder._fields

        # Find existing add_to_cart order
        order = SaleOrder.search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'add_to_cart'),
        ], limit=1)

        # ==========================================
        # IMPORTANT: Create order in add_to_cart stage
        # and set b2b_sale = True
        # ==========================================
        if not order:
            order_vals = {
                'partner_id': partner.id,
                'state': 'add_to_cart',
            }

            if has_b2b_sale:
                order_vals['b2b_sale'] = True

            order = SaleOrder.create(order_vals)

        else:
            # Existing add_to_cart order holeo b2b_sale True kore dao
            write_vals = {
                'state': 'add_to_cart',
            }

            if has_b2b_sale:
                write_vals['b2b_sale'] = True

            order.write(write_vals)

        existing_line = order.order_line.filtered(
            lambda line: line.product_id.id == product.id
        )

        if existing_line:
            line = existing_line[0]

            # Buy Now hole replace qty
            # Add to Cart hole also current selected qty set kortesi
            new_qty = quantity

            line.sudo().write({
                'product_uom_qty': new_qty,
            })

        else:
            line = SaleOrderLine.create({
                'order_id': order.id,
                'product_id': product.id,
                'product_uom_qty': quantity,
                'product_uom': product.uom_id.id,
            })

        return {
            'success': True,
            'order_id': order.id,
            'state': order.state,
            'b2b_sale': bool(order.b2b_sale) if has_b2b_sale else False,
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