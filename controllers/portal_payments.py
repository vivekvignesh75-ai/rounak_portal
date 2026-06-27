# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class RounakPortalPayments(CustomerPortal):

    @http.route("/my/rounak/payments", type="http", auth="user", website=True)
    def portal_payments(self, **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        tokens = request.env["payment.token"].sudo().search([
            ("partner_id", "child_of", partner.id),
        ])
        bank_details = {
            "emirates_nbd": {
                "bank": "Emirates NBD",
                "account_name": "Rounak Computers LLC",
                "iban": "AE12 0260 0010 1234 5678 901",
                "swift": "EABORAEAXXX",
            },
            "fab": {
                "bank": "First Abu Dhabi Bank",
                "account_name": "Rounak Computers LLC",
                "iban": "AE34 0350 0000 0620 1234 567",
                "swift": "NBABORAEAXXX",
            },
        }

        values = {
            "page_name": "rounak_payments",
            "tokens": tokens,
            "bank_details": bank_details,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_payments", values)
