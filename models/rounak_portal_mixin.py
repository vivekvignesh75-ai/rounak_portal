# -*- coding: utf-8 -*-
"""Shared helpers for portal badge counts and KPI queries."""
from odoo import api, fields, models


class RounakPortalMixin(models.AbstractModel):
    _name = "rounak.portal.mixin"
    _description = "Rounak Portal Helper Mixin"

    @api.model
    def _portal_partner(self):
        return self.env.user.partner_id.commercial_partner_id

    @api.model
    def _portal_kpis(self):
        partner = self._portal_partner()
        pid = partner.id
        SO = self.env["sale.order"].sudo()
        AM = self.env["account.move"].sudo()
        child_ids = partner.child_ids.ids + [pid]

        pending_quotes = SO.search_count([
            ("partner_id", "in", child_ids),
            ("state", "in", ("draft", "sent")),
        ])
        open_orders = SO.search_count([
            ("partner_id", "in", child_ids),
            ("state", "=", "sale"),
        ])
        due_invoices = AM.search_count([
            ("partner_id", "in", child_ids),
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("payment_state", "not in", ("paid", "reversed")),
        ])
        overdue_invoices = AM.search_count([
            ("partner_id", "in", child_ids),
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("payment_state", "not in", ("paid", "reversed")),
            ("invoice_date_due", "<", fields.Date.today()),
        ])

        total_spend = 0.0
        paid_invoices = AM.search([
            ("partner_id", "in", child_ids),
            ("move_type", "=", "out_invoice"),
            ("state", "=", "posted"),
            ("payment_state", "=", "paid"),
        ])
        for inv in paid_invoices:
            total_spend += inv.amount_total_signed

        open_tickets = 0
        try:
            Ticket = self.env["sh.helpdesk.ticket"].sudo()
            open_tickets = Ticket.search_count([
                ("partner_id", "in", child_ids),
                ("stage_id.closed", "=", False),
            ])
        except Exception:
            pass

        active_subs = 0
        try:
            Sub = self.env["subscription.package"].sudo()
            active_subs = Sub.search_count([
                ("partner_id", "in", child_ids),
                ("stage", "in", ("progress", "new")),
            ])
        except Exception:
            pass

        return {
            "total_spend": total_spend,
            "pending_quotes": pending_quotes,
            "open_orders": open_orders,
            "due_invoices": due_invoices,
            "overdue_invoices": overdue_invoices,
            "open_tickets": open_tickets,
            "active_subs": active_subs,
            "credit_available": partner.rounak_credit_available,
            "credit_limit": partner.credit_limit,
            "next_renewal": False,
        }

    @api.model
    def _portal_badge_counts(self):
        kpis = self._portal_kpis()
        unread = self.env["rounak.notification"].get_unread_count()
        return {
            "quotes": kpis["pending_quotes"],
            "invoices": kpis["due_invoices"],
            "tickets": kpis["open_tickets"],
            "notifications": unread,
        }
