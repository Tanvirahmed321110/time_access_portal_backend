from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(
        selection_add=[
            ('add_to_cart', 'Add to Cart'),
        ],
        ondelete={
            'add_to_cart': 'set default',
        }
    )


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_b2b_portal_line = fields.Boolean(
        string="Is B2B Portal Product",
        compute="_compute_b2b_price_info",
        store=False,
    )

    price_type_label = fields.Char(
        string="Price Label",
        compute="_compute_b2b_price_info",
        store=False,
    )

    b2b_price = fields.Float(
        string="B2B Price",
        related="product_id.product_tmpl_id.b2b_price",
        readonly=True,
        store=False,
    )

    @api.depends('product_id')
    def _compute_b2b_price_info(self):
        for line in self:
            product = line.product_id
            template = product.product_tmpl_id if product else False

            is_b2b = False

            if template and 'is_b2b_portal' in template._fields:
                is_b2b = template.is_b2b_portal

            if product and 'is_b2b_portal' in product._fields:
                is_b2b = product.is_b2b_portal

            line.is_b2b_portal_line = is_b2b
            line.price_type_label = "B2B Price" if is_b2b else "Unit Price"

    @api.depends(
        'product_id',
        'product_uom',
        'product_uom_qty',
        'order_id.partner_id',
        'order_id.pricelist_id',
        'order_id.date_order',
        'order_id.company_id',
    )
    def _compute_price_unit(self):
        super()._compute_price_unit()

        for line in self:
            if not line.product_id:
                continue

            product = line.product_id
            template = product.product_tmpl_id

            is_b2b_portal = False
            b2b_price = 0.0

            if 'is_b2b_portal' in template._fields:
                is_b2b_portal = template.is_b2b_portal

            if 'b2b_price' in template._fields:
                b2b_price = template.b2b_price or 0.0

            if 'is_b2b_portal' in product._fields:
                is_b2b_portal = product.is_b2b_portal

            if 'b2b_price' in product._fields:
                b2b_price = product.b2b_price or 0.0

            if is_b2b_portal:
                line.price_unit = b2b_price
            else:
                line.price_unit = product.lst_price or 0.0