from odoo import http
from odoo.http import request
from odoo.addons.time_access_portal.utilitis.pagination import get_pager

class TimeAccessPortal(http.Controller):

    @http.route('/index', type='http', auth='user', website=True)
    def index_f(self, sort='default', b2b_category=None, **kw):

        if (
                request.env.user.has_group('time_access_portal.group_b2b_general_user')
                and not request.env.user.has_group('time_access_portal.group_b2b_management')
        ):
            return request.redirect('/web')

        domain = [
            ('is_b2b_portal', '=', True)
        ]

        selected_category = False

        # >>> CHANGE: case-insensitive unique category list
        b2b_products = request.env['product.template'].sudo().search([
            ('is_b2b_portal', '=', True),
            ('b2b_category', '!=', False),
        ])
        raw_categories = b2b_products.mapped('b2b_category')

        category_map = {}
        for cat in raw_categories:
            key = cat.strip().lower()
            if key not in category_map:
                category_map[key] = cat.strip()

        categories = sorted(category_map.values())

        # >>> CHANGE: case-insensitive filter match
        if b2b_category:
            key = b2b_category.strip().lower()
            if key in category_map:
                selected_category = category_map[key]
                domain.append(('b2b_category', '=ilike', selected_category))

        # =======  Product sort desc and asc  =========
        order_by = 'id desc'
        if sort == 'low-high':
            order_by = 'list_price asc, id asc'
        elif sort == 'high-low':
            order_by = 'list_price desc, id asc'

        pager_url_args = {}
        if sort != 'default':
            pager_url_args['sort'] = sort
        if selected_category:
            pager_url_args['b2b_category'] = selected_category

        per_page = int(kw.get('per_page', 75))
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

        partner = request.env.user.partner_id
        sale_order = request.env['sale.order'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'add_to_cart'),
        ], limit=1)

        cart_product_ids = sale_order.order_line.mapped('product_id').ids if sale_order else []

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
            'selected_category': selected_category,
            'cart_product_ids': cart_product_ids,
            'pager': pager,
            'total': total,

            'product_min_qty_map': product_min_qty_map,
            'product_stock_qty_map': product_stock_qty_map,
            'product_default_qty_map': product_default_qty_map,
        })