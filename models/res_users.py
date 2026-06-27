# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    rounak_2fa_enabled = fields.Boolean(string="Two-Factor Authentication", default=False)
