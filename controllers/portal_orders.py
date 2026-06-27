# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class RounakPortalOrders(CustomerPortal):

    @http.route("/my/rounak/orders", type="http", auth="user", website=True)
    def portal_orders(self, page=1, status="all", **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        SO = request.env["sale.order"].sudo()
        domain = [
            ("partner_id", "child_of", partner.id),
            ("state", "in", ("sale", "done")),
        ]

        if status == "in_progress":
            domain += [("state", "=", "sale"), ("invoice_status", "!=", "invoiced")]
        elif status == "done":
            domain += [("state", "=", "done")]
        elif status == "invoiced":
            domain += [("invoice_status", "=", "invoiced")]

        total = SO.search_count(domain)
        pager = portal_pager(
            url="/my/rounak/orders",
            url_args={"status": status},
            total=total,
            page=page,
            step=20,
        )
        orders = SO.search(
            domain, limit=20, offset=pager["offset"],
            order="date_order desc",
        )

        values = {
            "page_name": "rounak_orders",
            "orders": orders,
            "pager": pager,
            "status": status,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_orders", values)

    @http.route("/my/rounak/order/<int:order_id>", type="http", auth="user", website=True)
    def portal_order_detail(self, order_id, **kw):
        order = request.env["sale.order"].sudo().browse(order_id)
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        if order.partner_id.commercial_partner_id != partner:
            return request.redirect("/my/rounak/orders")

        values = {
            "page_name": "rounak_order_detail",
            "order": order,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_order_detail", values)
