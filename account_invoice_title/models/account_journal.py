# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
    _inherit = "account.journal"

    invoice_use_custom_title = fields.Boolean(string="Use Custom Invoice Title (PDF)")
    invoice_custom_title = fields.Char(string="Invoice PDF Title")

    credit_note_use_custom_title = fields.Boolean(string="Use Custom Credit Note Title (PDF)")
    credit_note_custom_title = fields.Char(string="Credit Note PDF Title")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._log_title_misconfig()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._log_title_misconfig()
        return res

    def _log_title_misconfig(self):
        for j in self:
            if j.invoice_use_custom_title and not (j.invoice_custom_title or "").strip():
                _logger.warning(
                    "[s3_invoice_pdf_titles] Journal %s: Invoice title enabled but title is empty",
                    j.display_name,
                )
            if j.credit_note_use_custom_title and not (j.credit_note_custom_title or "").strip():
                _logger.warning(
                    "[s3_invoice_pdf_titles] Journal %s: Credit note title enabled but title is empty",
                    j.display_name,
                )