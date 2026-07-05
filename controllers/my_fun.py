from odoo.http import request

def get_cart_count():
    partner = request.env.user.partner_id
    sale_order = request.env['sale.order'].sudo().search([
        ('partner_id', '=', partner.id),
        ('state', '=', 'add_to_cart'),
    ], limit=1)
    return len(sale_order.order_line) if sale_order else 0