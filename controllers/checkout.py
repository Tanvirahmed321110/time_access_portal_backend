from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    @http.route('/checkout', type='http', auth='user', website=True)
    def checkout_page(self, product_id=None, qty=1, **kw):
        partner = request.env.user.partner_id.sudo()

        order_line = None
        order_lines = []
        amount_total = 0.0
        is_buy_now = False

        # ===== Buy Now flow =====
        if product_id and str(product_id).isdigit():
            is_buy_now = True
            product = request.env['product.template'].sudo().browse(int(product_id))
            order_line = {
                'product': product,
                'qty': float(qty),
                'subtotal': product.list_price * float(qty),
            }
            amount_total = order_line['subtotal']

        # ===== Cart flow =====
        else:
            sale_order = request.env['sale.order'].sudo().search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'add_to_cart'),
            ], limit=1)

            if sale_order:
                order_lines = sale_order.order_line
                amount_total = sale_order.amount_total

        return request.render('time_access_portal.checkout_page', {
            'active_menu': 'checkout',
            'is_buy_now': is_buy_now,
            'order_line': order_line,
            'order_lines': order_lines,
            'amount_total': amount_total,
            'qty': qty,
            'product_id': product_id,
            'partner': partner,
        })


    @http.route('/cart/confirm', type='json', auth='user', website=True)
    def confirm_order(self, product_id=None, qty=1, **kw):
        partner = request.env.user.partner_id.sudo()

        name = kw.get('company_name', '').strip()
        mobile = kw.get('mobile', '').strip()
        email = kw.get('email', '').strip()
        street = kw.get('street', '').strip()

        # =====================================================
        # Update customer/contact from checkout form
        # =====================================================
        partner_vals = {}

        if name:
            partner_vals['name'] = name

        if mobile:
            partner_vals['phone'] = mobile
            partner_vals['mobile'] = mobile

        if email:
            partner_vals['email'] = email

        if street:
            partner_vals['street'] = street

        if partner_vals:
            partner.write(partner_vals)

        # =====================================================
        # Buy Now flow
        # =====================================================
        if product_id:
            product = request.env['product.product'].sudo().browse(int(product_id)).exists()

            if not product:
                return {
                    'success': False,
                    'error': 'Product not found',
                }

            order = request.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'state': 'draft',
                'b2b_sale': True,
            })

            b2b_price = product.product_tmpl_id.b2b_price or 0.0

            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'product_id': product.id,
                'product_uom_qty': float(qty or 1),
                'product_uom': product.uom_id.id,
                'price_unit': b2b_price,
            })

        # =====================================================
        # Cart flow
        # =====================================================
        else:
            order = request.env['sale.order'].sudo().search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'add_to_cart'),
            ], limit=1)

            if not order:
                return {
                    'success': False,
                    'error': 'No cart found',
                }

            order.sudo().write({
                'state': 'draft',
                'b2b_sale': True,
            })

            # Recalculate lines with B2B price
            for line in order.order_line:
                if line.product_id:
                    line.price_unit = line.product_id.product_tmpl_id.b2b_price or 0.0

        return {
            'success': True,
            'order_id': order.id,
        }