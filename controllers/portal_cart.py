# -*- coding: utf-8 -*-
from odoo import _, http
from odoo.http import request
from odoo.exceptions import UserError
from odoo.addons.portal.controllers.portal import CustomerPortal


class RounakPortalCart(CustomerPortal):

    def _get_cart_order(self):
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        return request.env["sale.order"].sudo().search(
            [
                ("partner_id", "child_of", partner.id),
                ("state", "=", "draft"),
                ("website_id", "!=", False),
            ],
            limit=1,
            order="create_date desc",
        )

    @http.route("/my/rounak/cart", type="http", auth="user", website=True)
    def portal_cart(self, **kw):
        order = self._get_cart_order()
        values = {
            "page_name": "rounak_cart",
            "order": order,
            "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
        }
        return request.render("rounak_portal.portal_cart", values)

    @http.route("/my/rounak/cart/update", type="http", auth="user",
                website=True, methods=["POST"])
    def portal_cart_update(self, line_id=0, qty=1, **kw):
        line = request.env["sale.order.line"].sudo().browse(int(line_id))
        partner = request.env["rounak.portal.mixin"]._portal_partner()
        if line and line.order_id.partner_id.commercial_partner_id == partner:
            qty = max(0, int(qty))
            if qty == 0:
                line.unlink()
            else:
                line.product_uom_qty = qty
        return request.redirect("/my/rounak/cart")

    @http.route("/my/rounak/cart/checkout", type="http", auth="user",
                website=True, methods=["POST"])
    def portal_cart_checkout(self, **kw):
        order = self._get_cart_order()
        if not order or not order.order_line:
            return request.redirect("/my/rounak/cart")

        partner = order.partner_id.commercial_partner_id

        if partner.rounak_transaction_blocked:
            return request.render("rounak_portal.portal_cart", {
                "page_name": "rounak_cart",
                "order": order,
                "error": _("Your account is currently blocked. Contact your account manager."),
                "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
            })

        if partner.credit_limit and (
            partner.rounak_credit_balance + order.amount_total > partner.credit_limit
        ):
            return request.render("rounak_portal.portal_cart", {
                "page_name": "rounak_cart",
                "order": order,
                "error": _(
                    "Order exceeds credit limit. Available: AED %(avail)s, Order: AED %(total)s",
                    avail=partner.rounak_credit_available,
                    total=order.amount_total,
                ),
                "badges": request.env["rounak.portal.mixin"]._portal_badge_counts(),
            })

        flow = request.env["rounak.order.flow"].sudo().create({
            "partner_id": partner.id,
            "sale_order_id": order.id,
            "amount_total": order.amount_total,
            "currency_id": order.currency_id.id,
            "state": "payment_pending",
        })

        request.env["rounak.notification"].emit(
            code="order_payment_pending",
            user_ids=request.env.user.ids,
            title=_("Order %s submitted", order.name),
            body=_("Your order for AED %s is awaiting payment.", order.amount_total),
            res_model="sale.order",
            res_id=order.id,
        )

        return request.redirect("/my/rounak/orders")

    @http.route("/my/rounak/cart/discount-request", type="http", auth="user",
                website=True, methods=["POST"])
    def portal_cart_discount_request(self, discount_pct=0, reason="", **kw):
        order = self._get_cart_order()
        if not order:
            return request.redirect("/my/rounak/cart")

        pct = float(discount_pct or 0)
        if pct <= 0:
            return request.redirect("/my/rounak/cart")

        partner = order.partner_id.commercial_partner_id

        dr = request.env["discount.request"].sudo().create({
            "sale_order_id": order.id,
            "partner_id": partner.id,
            "requested_discount": pct,
            "reason": reason,
        })

        request.env["rounak.audit.log"].log(
            "discount_request",
            _("Discount request: %s%% on %s", pct, order.name),
            res_model="discount.request",
            res_id=dr.id,
            partner_id=partner.id,
        )

        request.env["rounak.notification"].emit(
            code="discount_requested",
            user_ids=order.user_id.ids if order.user_id else [],
            title=_("Discount request on %s", order.name),
            body=_("Customer %s requested %s%% discount. Reason: %s", partner.name, pct, reason),
            res_model="discount.request",
            res_id=dr.id,
        )

        return request.redirect("/my/rounak/cart")
