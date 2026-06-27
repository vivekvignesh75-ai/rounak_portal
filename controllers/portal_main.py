# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class RounakPortalMain(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        mixin = request.env["rounak.portal.mixin"]
        badges = mixin._portal_badge_counts()
        values.update({
            "rounak_badge_quotes": badges["quotes"],
            "rounak_badge_invoices": badges["invoices"],
            "rounak_badge_tickets": badges["tickets"],
            "rounak_badge_notifications": badges["notifications"],
        })
        return values

    @http.route("/my/rounak/dashboard", type="http", auth="user", website=True)
    def portal_dashboard(self, **kw):
        mixin = request.env["rounak.portal.mixin"]
        kpis = mixin._portal_kpis()
        badges = mixin._portal_badge_counts()

        notifications = request.env["rounak.notification"].sudo().search(
            [("user_id", "=", request.env.uid), ("is_read", "=", False)],
            limit=10, order="create_date desc",
        )

        partner = mixin._portal_partner()
        recent_orders = request.env["sale.order"].sudo().search(
            [("partner_id", "child_of", partner.id), ("state", "=", "sale")],
            limit=5, order="date_order desc",
        )

        values = {
            "page_name": "rounak_dashboard",
            "kpis": kpis,
            "badges": badges,
            "notifications": notifications,
            "recent_orders": recent_orders,
            "partner": partner,
        }
        return request.render("rounak_portal.portal_dashboard", values)
