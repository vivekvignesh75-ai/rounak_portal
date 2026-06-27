# -*- coding: utf-8 -*-
from odoo import models
from odoo.http import request
from werkzeug.utils import redirect


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _frontend_pre_dispatch(cls):
        super()._frontend_pre_dispatch()
        if not request.uid or request.uid == request.env.ref("base.public_user").id:
            return
        path = request.httprequest.path
        if not path.startswith("/my/rounak/") or path == "/my/rounak/blocked":
            return
        partner = request.env.user.partner_id.commercial_partner_id
        if partner.rounak_portal_locked:
            raise redirect("/my/rounak/blocked")
