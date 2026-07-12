from odoo import models, fields, api
from datetime import date

class ProductProductInherit(models.Model):
    _inherit = 'product.template'
    _order = 'create_date desc'

    is_b2b_portal = fields.Boolean(string='is b2b portal')
    b2b_price = fields.Float(
        string='B2B  Price',
        digits='Product Price',
        tracking=True,
        groups='time_access_portal.group_b2b_management'
    )
    b2b_qty = fields.Integer(string='B2B  Qty')
    b2b_category = fields.Char(string='B2B  Category')
