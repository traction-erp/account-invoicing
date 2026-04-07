# -*- coding: utf-8 -*-
import base64
import io
import re
import zipfile

from odoo import api, fields, models, _
from odoo.exceptions import UserError


def _safe_filename(name: str) -> str:
    name = (name or "").strip()
    name = re.sub(r"[^\w\-. ]+", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name or "invoice"


class AccountMovePrintLangWizard(models.TransientModel):
    _name = "account.move.print.lang.wizard"
    _description = "Print Invoice PDFs (Fresh Render) with Language"

    lang_id = fields.Many2one("res.lang", string="Output Language", required=True)
    move_ids = fields.Many2many(
        "account.move",
        string="Invoices",
        required=True,
        domain="[('move_type', 'in', ('out_invoice','out_refund','out_receipt'))]",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get("active_model")
        active_ids = self.env.context.get("active_ids") or []
        if active_model != "account.move" or not active_ids:
            return res

        moves = self.env["account.move"].browse(active_ids).exists()
        moves = moves.filtered(lambda m: m.move_type in ("out_invoice", "out_refund", "out_receipt"))
        if not moves:
            raise UserError(_("Please select at least one customer invoice/credit note/receipt."))

        res["move_ids"] = [(6, 0, moves.ids)]

        # Default to USER language (per your requirement)
        lang_code = self.env.user.lang or "en_US"
        lang = self.env["res.lang"].search([("code", "=", lang_code)], limit=1)
        res["lang_id"] = lang.id if lang else self.env["res.lang"].search([], limit=1).id
        return res

    def action_download_zip(self):
        self.ensure_one()
        moves = self.move_ids.exists()
        if not moves:
            raise UserError(_("No invoices selected."))

        report = self.env.ref("account.account_invoices", raise_if_not_found=False)
        if not report:
            raise UserError(_("Could not find invoice report action 'account.account_invoices'."))

        lang_code = self.lang_id.code

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for move in moves:
                ctx = dict(self.env.context or {})
                ctx.update({
                    "lang": lang_code,              # helps translations at env level
                    "report_lang": lang_code,       # your QWeb override will honor this
                    "force_report_rendering": True, # bypass cached pdf reuse
                    "no_report_attachment": True,   # avoid saving report attachment (where honored)
                    "allowed_company_ids": [move.company_id.id],
                    "force_company": move.company_id.id,
                    "company_id": move.company_id.id,
                })

                pdf_content, _content_type = report.with_company(move.company_id).with_context(ctx) \
                    ._render_qweb_pdf(report.xml_id, res_ids=[move.id])

                inv_name = _safe_filename(move.name or move.display_name)
                filename = f"{inv_name}_{lang_code}.pdf"
                zf.writestr(filename, pdf_content)

        zip_bytes = buf.getvalue()
        if not zip_bytes:
            raise UserError(_("Failed to generate the ZIP file."))

        zip_name = f"invoices_{lang_code}.zip"
        attachment = self.env["ir.attachment"].create({
            "name": zip_name,
            "type": "binary",
            "datas": base64.b64encode(zip_bytes),
            "mimetype": "application/zip",
            "res_model": self._name,
            "res_id": self.id,
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }
