from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    @http.route('/cart', type='http', auth='user', website=True)
    def index_f(self, **kw):
        return request.render('time_access_portal.cart_page', {
            '': '',
        })


    # ==================  Add To Cart  ===================
    @http.route('/cart/add', type='json', auth='user', website=True)
    def add_to_cart(self, product_id, quantity=1, **kw):
        partner = request.env.user.partner_id

        # Existing draft order আছে কিনা check
        order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'draft'),
        ], limit=1)

        # না থাকলে নতুন draft order বানাও
        if not order:
            order = request.env['sale.order'].sudo().create({
                'partner_id': partner.id,
                'state': 'draft',
            })

        # Product আগে আছে কিনা check
        existing_line = order.order_line.filtered(
            lambda l: l.product_id.id == product_id
        )

        if existing_line:
            # থাকলে quantity বাড়াও
            existing_line.product_uom_qty += quantity
        else:
            # না থাকলে নতুন line add করো
            request.env['sale.order.line'].sudo().create({
                'order_id': order.id,
                'product_id': product_id,
                'product_uom_qty': quantity,
            })

        return {'success': True, 'order_id': order.id}
