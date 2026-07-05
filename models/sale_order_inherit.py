from odoo import models, fields


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