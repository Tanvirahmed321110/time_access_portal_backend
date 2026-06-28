from odoo import models, fields, api
from datetime import date

class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    is_b2b_category = fields.Boolean(string='Is B2B Category?')

