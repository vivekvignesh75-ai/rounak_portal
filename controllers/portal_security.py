# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class RounakPortalSecurity(CustomerPortal):

    @http.route("/my/rounak/security", type="http", auth="user", website=True)
    def portal_security(self, **kw):
        user = request.env.user
        values = {
            "page_name": "rounak_security",
            "user": user,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_security", values)

    @http.route("/my/rounak/security/toggle_2fa", type="http", auth="user",
                website=True, methods=["POST"])
    def portal_toggle_2fa(self, **kw):
        user = request.env.user
        user.sudo().write({"rounak_2fa_enabled": not user.rounak_2fa_enabled})
        return request.redirect("/my/rounak/security")
