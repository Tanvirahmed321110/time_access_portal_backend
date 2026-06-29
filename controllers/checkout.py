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
                ('state', '=', 'draft'),
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
    @http.route('/cart/confirm', type='json', auth='user', website=True)
    def confirm_order(self, product_id=None, qty=1, **kw):
        partner = request.env.user.partner_id

        company_name = kw.get('company_name', '').strip()
        bin_number = kw.get('bin_number', '').strip()
        phone = kw.get('phone', '').strip()
        email = kw.get('email', '').strip()
        shipping_address = kw.get('shipping_address', '').strip()

        current_company = request.env.company.sudo()

        if current_company:
            current_company.write({
                'name': company_name if company_name else current_company.name,
                'vat': bin_number if bin_number else current_company.vat,
                'phone': phone if phone else current_company.phone,
                'email': email if email else current_company.email,
                'street': shipping_address if shipping_address else current_company.street
            })

        # ===== Buy Now flow =====
        if product_id:
            order = request.env['sale.order'].sudo().create({
                'partner_id': partner.id,
            })
            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'product_id': int(product_id),
                'product_uom_qty': float(qty),
            })

        # ===== Cart flow =====
        else:
            order = request.env['sale.order'].sudo().search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'draft'),
            ], limit=1)

            if not order:
                return {'success': False, 'error': 'No cart found'}

        order.action_confirm()
        return {'success': True, 'order_id': order.id}