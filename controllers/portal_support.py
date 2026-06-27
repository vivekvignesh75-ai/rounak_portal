# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class RounakPortalSupport(CustomerPortal):

    @http.route("/my/rounak/support", type="http", auth="user", website=True)
    def portal_support(self, page=1, status="all", **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        Ticket = request.env["sh.helpdesk.ticket"].sudo()
        domain = [("partner_id", "child_of", partner.id)]

        if status == "open":
            domain += [("stage_id.closed", "=", False)]
        elif status == "closed":
            domain += [("stage_id.closed", "=", True)]

        total = Ticket.search_count(domain)
        pager = portal_pager(
            url="/my/rounak/support",
            url_args={"status": status},
            total=total,
            page=page,
            step=20,
        )
        tickets = Ticket.search(
            domain, limit=20, offset=pager["offset"],
            order="create_date desc",
        )

        urgent_count = Ticket.search_count([
            ("partner_id", "child_of", partner.id),
            ("stage_id.closed", "=", False),
            ("priority", "!=", False),
        ])

        values = {
            "page_name": "rounak_support",
            "tickets": tickets,
            "pager": pager,
            "status": status,
            "urgent_count": urgent_count,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_support", values)

    @http.route("/my/rounak/support/create", type="http", auth="user",
                website=True, methods=["POST"])
    def portal_support_create(self, **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        vals = {
            "partner_id": partner.id,
            "person_name": request.env.user.name,
            "email": request.env.user.email,
            "subject": kw.get("subject", ""),
            "description": kw.get("description", ""),
        }
        if kw.get("team_id"):
            vals["team_id"] = int(kw["team_id"])

        ticket = request.env["sh.helpdesk.ticket"].sudo().create(vals)

        request.env["rounak.notification"].emit(
            code="ticket_created",
            user_ids=request.env.user.ids,
            title=_("Support ticket #%s created", ticket.name),
            body=_("Your ticket '%s' has been submitted.", kw.get("subject", "")),
            res_model="sh.helpdesk.ticket",
            res_id=ticket.id,
        )

        return request.redirect("/my/rounak/support")
