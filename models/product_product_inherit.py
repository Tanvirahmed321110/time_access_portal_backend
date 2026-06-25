# models/product_product.py

from odoo import models, fields, api


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('default_code'):
                vals['default_code'] = self.env['ir.sequence'].next_by_code(
                    'product.default.code.auto'
                ) or '/'

        return super().create(vals_list)