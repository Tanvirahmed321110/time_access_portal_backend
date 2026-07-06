from odoo import api, fields, models


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

    b2b_sale = fields.Boolean(
        string="B2B Sale",
        tracking=True,
        readonly=True,
    )

    @api.onchange('b2b_sale')
    def _onchange_b2b_sale(self):
        """
        When B2B Sale is checked/unchecked,
        reload sale order line unit prices.
        """
        for order in self:
            for line in order.order_line:
                line._compute_price_unit()

    def write(self, vals):
        res = super().write(vals)

        if 'b2b_sale' in vals:
            for order in self:
                order.order_line._compute_price_unit()

        return res


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
        digits='Product Price',
    )

    @api.depends('order_id.b2b_sale', 'product_id')
    def _compute_b2b_price_info(self):
        for line in self:
            line.price_type_label = "B2B Price" if line.order_id.b2b_sale else "Unit Price"
            line.is_b2b_portal_line = bool(line.order_id.b2b_sale)

    @api.depends(
        'product_id',
        'product_uom',
        'product_uom_qty',
        'order_id.partner_id',
        'order_id.pricelist_id',
        'order_id.date_order',
        'order_id.company_id',
        'order_id.currency_id',
        'order_id.b2b_sale',
        'product_id.product_tmpl_id.b2b_price',
    )
    def _compute_price_unit(self):
        """
        Logic:
        If Sale Order B2B Sale = True:
            Unit Price = Product B2B Price
            Amount = B2B Price * Quantity

        Else:
            Unit Price = Normal Odoo Price / Pricelist Price
            Amount = Unit Price * Quantity
        """

        # First let Odoo calculate normal price_unit
        super()._compute_price_unit()

        # Then override only B2B sale order lines
        for line in self:
            if line.display_type or not line.product_id:
                continue

            if line.order_id.b2b_sale:
                line.price_unit = line.product_id.product_tmpl_id.b2b_price or 0.0