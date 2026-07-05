from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    @http.route('/checkout', type='http', auth='user', website=True)
    def checkout_page(self, product_id=None, qty=1, **kw):
        partner = request.env.user.partner_id
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
            'order_line': order_line,  # Buy Now এর জন্য
            'order_lines': order_lines,  # Cart এর জন্য
            'amount_total': amount_total,
            'qty': qty,
            'product_id': product_id,
        })

    # ===== Cart flow =====
    # ===== Confirm Cart / Buy Now as Draft Quotation =====
    @http.route('/cart/confirm', type='json', auth='user', website=True)
    def confirm_order(self, product_id=None, qty=1, **kw):
        partner = request.env.user.partner_id

        company_name = kw.get('company_name', '').strip()
        phone = kw.get('phone', '').strip()
        email = kw.get('email', '').strip()
        shipping_address = kw.get('shipping_address', '').strip()

        current_company = request.env.company.sudo()

        if current_company:
            vals = {}

            if company_name:
                vals['name'] = company_name
            if phone:
                vals['phone'] = phone
            if email:
                vals['email'] = email
            if shipping_address:
                vals['street'] = shipping_address

            if vals:
                current_company.write(vals)

        # ===== Buy Now flow =====
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
            })

            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'product_id': product.id,
                'product_uom_qty': float(qty or 1),
                'product_uom': product.uom_id.id,
                'price_unit': product.lst_price,
            })

        # ===== Cart flow =====
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

            # Add to Cart state theke Draft/Quotation stage e niye jabe
            order.sudo().write({
                'state': 'draft',
            })

        return {
            'success': True,
            'order_id': order.id,
        }