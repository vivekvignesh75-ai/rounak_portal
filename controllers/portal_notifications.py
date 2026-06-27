# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class RounakPortalNotifications(CustomerPortal):

    @http.route("/my/rounak/notifications", type="http", auth="user", website=True)
    def portal_notifications(self, page=1, **kw):
        Notif = request.env["rounak.notification"].sudo()
        domain = [("user_id", "=", request.env.uid)]

        total = Notif.search_count(domain)
        pager = portal_pager(
            url="/my/rounak/notifications",
            total=total,
            page=page,
            step=20,
        )
        notifications = Notif.search(
            domain, limit=20, offset=pager["offset"],
            order="create_date desc",
        )

        values = {
            "page_name": "rounak_notifications",
            "notifications": notifications,
            "pager": pager,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_notifications", values)

    @http.route("/my/rounak/notifications/mark_read", type="http", auth="user",
                website=True, methods=["POST"])
    def portal_mark_all_read(self, **kw):
        request.env["rounak.notification"].mark_all_read()
        return request.redirect("/my/rounak/notifications")

    @http.route("/my/rounak/notification/<int:notif_id>/read", type="http",
                auth="user", website=True, methods=["POST"])
    def portal_mark_one_read(self, notif_id, **kw):
        notif = request.env["rounak.notification"].sudo().browse(notif_id)
        if notif.user_id.id == request.env.uid:
            notif.action_mark_read()
        return request.redirect("/my/rounak/notifications")
