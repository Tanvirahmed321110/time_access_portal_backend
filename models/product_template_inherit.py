from odoo import models, fields, api
from datetime import date

class ProductProductInherit(models.Model):
    _inherit = 'product.template'
    _order = 'create_date desc'

    is_b2b_portal = fields.Boolean(string='is b2b portal?')

    # # For Userlink links page
    # live_link  = fields.Char(string='Live Link')
    # github_link = fields.Char(string='Github Repo Link')
    # dev_link = fields.Char(string='Dev Server Link')
    #
    #
    # custom_priority = fields.Selection([
    #     ('normal','normal'),
    #     ('medium','medium'),
    #     ('high','high'),
    #     ('urgent','urgent'),
    # ], string=' Priority',default='normal')
    #
    # custom_status = fields.Selection([
    #     ('planning', 'Planning'),
    #     ('in_progress', 'In Progress'),
    #     ('review', 'Under Review'),
    #     ('completed', 'Completed'),
    #     ('cancelled', 'Cancelled'),
    # ], string='Project Status', default='planning')
    #
    # # assign members
    # assigned_user_ids = fields.Many2many(
    #     'res.users',
    #     string='Assigned Users'
    # )
    #
    # # 🔥 Remaining Days Field
    # remaining_days = fields.Integer(
    #     string='Remaining Days',
    #     compute='_compute_remaining_days',
    #     store=True,
    #     readonly=True,
    # )
    #
    # @api.depends('date')
    # def _compute_remaining_days(self):
    #     today = date.today()
    #
    #     for rec in self:
    #         if rec.date:
    #             rec.remaining_days = (rec.date - today).days
    #         else:
    #             rec.remaining_days = 0
    #
    # allocated_hours = fields.Float(
    #     compute="_compute_allocated_hours",
    #     store=True,
    #     readonly=False
    # )

    # @api.depends("date_start", "date")
    # def _compute_allocated_hours(self):
    #     for rec in self:
    #         if rec.date_start and rec.date:
    #             delta = rec.date - rec.date_start
    #             rec.allocated_hours = delta.days * 8
    #         else:
    #             rec.allocated_hours = 0.0