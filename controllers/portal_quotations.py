# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class RounakPortalQuotations(CustomerPortal):

    @http.route("/my/rounak/quotations", type="http", auth="user", website=True)
    def portal_quotations(self, page=1, status="all", **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        SO = request.env["sale.order"].sudo()
        domain = [("partner_id", "child_of", partner.id)]

        if status == "pending":
            domain += [("state", "in", ("draft", "sent"))]
        elif status == "accepted":
            domain += [("state", "=", "sale")]
        elif status == "expired":
            domain += [("state", "=", "cancel")]

        total = SO.search_count(domain)
        pager = portal_pager(
            url="/my/rounak/quotations",
            url_args={"status": status},
            total=total,
            page=page,
            step=20,
        )
        quotations = SO.search(
            domain, limit=20, offset=pager["offset"],
            order="create_date desc",
        )

        pending_count = SO.search_count([
            ("partner_id", "child_of", partner.id),
            ("state", "in", ("draft", "sent")),
        ])

        values = {
            "page_name": "rounak_quotations",
            "quotations": quotations,
            "pager": pager,
            "status": status,
            "pending_count": pending_count,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_quotations", values)

    @http.route("/my/rounak/quotation/<int:order_id>/accept", type="http",
                auth="user", website=True, methods=["POST"])
    def portal_quotation_accept(self, order_id, **kw):
        order = request.env["sale.order"].sudo().browse(order_id)
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        if order.partner_id.commercial_partner_id != partner:
            return request.redirect("/my/rounak/quotations")
        order.action_confirm()
        request.env["rounak.notification"].emit(
            code="quote_accepted",
            user_ids=order.user_id.ids if order.user_id else [],
            title=_("Quotation %s accepted", order.name),
            body=_("Customer %s accepted quotation %s.", partner.name, order.name),
            res_model="sale.order",
            res_id=order.id,
        )
        return request.redirect("/my/rounak/quotations?status=accepted")

    @http.route("/my/rounak/quotation/<int:order_id>/reject", type="http",
                auth="user", website=True, methods=["POST"])
    def portal_quotation_reject(self, order_id, **kw):
        order = request.env["sale.order"].sudo().browse(order_id)
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        if order.partner_id.commercial_partner_id != partner:
            return request.redirect("/my/rounak/quotations")
        order.action_cancel()
        request.env["rounak.notification"].emit(
            code="quote_rejected",
            user_ids=order.user_id.ids if order.user_id else [],
            title=_("Quotation %s rejected", order.name),
            body=_("Customer %s rejected quotation %s.", partner.name, order.name),
            res_model="sale.order",
            res_id=order.id,
        )
        return request.redirect("/my/rounak/quotations")
