# -*- coding: utf-8 -*-
"""Portal lock enforcement: blocked customers see a restricted page."""
from odoo import http
from odoo.http import request


class RounakPortalLock(http.Controller):

    @http.route("/my/rounak/blocked", type="http", auth="user", website=True)
    def portal_blocked(self, **kw):
        partner = request.env.user.partner_id.commercial_partner_id
        return request.render("rounak_portal.portal_blocked", {
            "page_name": "rounak_blocked",
            "partner": partner,
            "reason": partner.rounak_block_reason or "",
        })
