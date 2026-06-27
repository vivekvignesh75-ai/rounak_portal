# -*- coding: utf-8 -*-
"""Multi-currency context helper for portal pages."""
from odoo import api, fields, models


class RounakPortalCurrency(models.AbstractModel):
    _name = "rounak.portal.currency"
    _description = "Portal Currency Helper"

    @api.model
    def get_portal_currency(self):
        icp = self.env["ir.config_parameter"].sudo()
        code = icp.get_param("rounak_portal.display_currency", "AED")
        currency = self.env["res.currency"].sudo().search(
            [("name", "=", code), ("active", "=", True)], limit=1,
        )
        return currency or self.env.company.currency_id

    @api.model
    def convert_amount(self, amount, from_currency, to_currency=None):
        if not to_currency:
            to_currency = self.get_portal_currency()
        if from_currency == to_currency:
            return amount
        return from_currency._convert(
            amount,
            to_currency,
            self.env.company,
            fields.Date.today(),
        )

    @api.model
    def format_amount(self, amount, currency=None):
        if not currency:
            currency = self.get_portal_currency()
        return "{} {:,.2f}".format(currency.symbol or currency.name, amount)

    @api.model
    def available_currencies(self):
        codes = ["AED", "USD", "EUR", "GBP"]
        return self.env["res.currency"].sudo().search([
            ("name", "in", codes), ("active", "=", True),
        ])
