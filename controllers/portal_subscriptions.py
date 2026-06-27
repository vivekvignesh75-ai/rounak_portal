# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class RounakPortalSubscriptions(CustomerPortal):

    @http.route("/my/rounak/subscriptions", type="http", auth="user", website=True)
    def portal_subscriptions(self, page=1, **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        Sub = request.env["subscription.package"].sudo()
        domain = [("partner_id", "child_of", partner.id)]

        total = Sub.search_count(domain)
        pager = portal_pager(
            url="/my/rounak/subscriptions",
            total=total,
            page=page,
            step=20,
        )
        subs = Sub.search(
            domain, limit=20, offset=pager["offset"],
            order="create_date desc",
        )

        values = {
            "page_name": "rounak_subscriptions",
            "subscriptions": subs,
            "pager": pager,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_subscriptions", values)

    @http.route("/my/rounak/subscription/<int:sub_id>/increase", type="http",
                auth="user", website=True, methods=["POST"])
    def portal_subscription_increase(self, sub_id, qty=1, **kw):
        sub = request.env["subscription.package"].sudo().browse(sub_id)
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        if sub.partner_id.commercial_partner_id != partner:
            return request.redirect("/my/rounak/subscriptions")

        try:
            request.env["subscription.package.request"].sudo().create({
                "subscription_id": sub.id,
                "partner_id": partner.id,
                "request_type": "qty_increase",
                "requested_qty": int(qty),
            })
        except Exception:
            pass

        return request.redirect("/my/rounak/subscriptions")
