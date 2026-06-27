# -*- coding: utf-8 -*-
from odoo import fields, http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class RounakPortalInvoices(CustomerPortal):

    @http.route("/my/rounak/invoices", type="http", auth="user", website=True)
    def portal_invoices(self, page=1, status="all", **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        AM = request.env["account.move"].sudo()
        domain = [
            ("partner_id", "child_of", partner.id),
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
        ]

        if status == "paid":
            domain += [("payment_state", "=", "paid")]
        elif status == "due":
            domain += [("payment_state", "not in", ("paid", "reversed"))]
        elif status == "overdue":
            domain += [
                ("payment_state", "not in", ("paid", "reversed")),
                ("invoice_date_due", "<", fields.Date.today()),
            ]

        total = AM.search_count(domain)
        pager = portal_pager(
            url="/my/rounak/invoices",
            url_args={"status": status},
            total=total,
            page=page,
            step=20,
        )
        invoices = AM.search(
            domain, limit=20, offset=pager["offset"],
            order="invoice_date desc",
        )

        total_due = sum(
            inv.amount_residual
            for inv in AM.search([
                ("partner_id", "child_of", partner.id),
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("payment_state", "not in", ("paid", "reversed")),
            ])
        )

        values = {
            "page_name": "rounak_invoices",
            "invoices": invoices,
            "pager": pager,
            "status": status,
            "total_due": total_due,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_invoices", values)
