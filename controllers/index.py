from odoo import http
from odoo.http import request
from odoo.addons.time_access_portal.utilitis.pagination import get_pager

class TimeAccessPortal(http.Controller):

    @http.route('/index', type='http', auth='user', website=True)
    def index_f(self, sort='default', category_id=None, **kw):

        # Block B2B General User from /index portal
        if (
                request.env.user.has_group('time_access_portal.group_b2b_general_user')
                and not request.env.user.has_group('time_access_portal.group_b2b_management')
        ):
            return request.redirect('/web')

        domain = [
            ('is_b2b_portal', '=', True)
        ]

        selected_category_id = False

        # Only checked B2B categories will show in UI
        categories = request.env['product.category'].sudo().search([
            ('is_b2b_category', '=', True)
        ])

        # Category filter
        if category_id and str(category_id).isdigit():
            category = request.env['product.category'].sudo().search([
                ('id', '=', int(category_id)),
                ('is_b2b_category', '=', True),
            ], limit=1)

            if category:
                selected_category_id = category.id
                domain.append(('categ_id', 'child_of', selected_category_id))

        #=======  Product sort desc and asc  =========
        order_by = 'id desc'

        if sort == 'low-high':
            order_by = 'list_price asc, id asc'
        elif sort == 'high-low':
            order_by = 'list_price desc, id asc'

        # ===== Pagination Setup =====

        pager_url_args = {}
        if sort != 'default':
            pager_url_args['sort'] = sort
        if selected_category_id:
            pager_url_args['category_id'] = selected_category_id

        per_page = int(kw.get('per_page', 15))
        total = request.env['product.template'].sudo().search_count(domain)

        pager = get_pager(
            url='/index',
            total=total,
            page=kw.get('page', 1),
            per_page=per_page,
            url_args=pager_url_args,
        )

        products = request.env['product.template'].sudo().search(
            domain,
            order=order_by,
            offset=pager['offset'],
            limit=pager['per_page']
        )

        # for sale order check
        partner = request.env.user.partner_id
        sale_order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'add_to_cart'),
        ], limit=1)

        cart_product_ids = sale_order.order_line.mapped('product_id').ids if sale_order else []

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


        return request.render('time_access_portal.index_page', {
            'active_menu': 'products',
            'products': products,
            'sort': sort,
            'categories': categories,
            'selected_category_id': selected_category_id,
            'cart_product_ids': cart_product_ids,
            'pager': pager,
            'total': total,

            # B2B qty values for XML
            'product_min_qty_map': product_min_qty_map,
            'product_stock_qty_map': product_stock_qty_map,
            'product_default_qty_map': product_default_qty_map,
        })