# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class RounakPortalSettings(CustomerPortal):

    @http.route("/my/rounak/settings", type="http", auth="user", website=True)
    def portal_settings(self, **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        values = {
            "page_name": "rounak_settings",
            "partner": partner,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_settings", values)

    @http.route("/my/rounak/trade-license", type="http", auth="user", website=True)
    def portal_trade_license(self, **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        values = {
            "page_name": "rounak_trade_license",
            "partner": partner,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_trade_license", values)

    @http.route("/my/rounak/domains", type="http", auth="user", website=True)
    def portal_domains(self, **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        domains = request.env["res.partner.domain"].sudo().search([
            ("partner_id", "child_of", partner.id),
        ])
        values = {
            "page_name": "rounak_domains",
            "domains": domains,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_domains", values)

    @http.route("/my/rounak/invoice-profiles", type="http", auth="user", website=True)
    def portal_invoice_profiles(self, **kw):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        profiles = request.env["account.invoice.profile"].sudo().search([
            ("partner_id", "child_of", partner.id),
        ])
        values = {
            "page_name": "rounak_invoice_profiles",
            "profiles": profiles,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_invoice_profiles", values)

    @http.route("/my/rounak/terms", type="http", auth="user", website=True)
    def portal_terms(self, **kw):
        values = {
            "page_name": "rounak_terms",
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_terms", values)
