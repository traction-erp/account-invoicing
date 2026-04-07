# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    def _pdf_custom_title(self):
        """Return the journal-defined custom title for invoice/credit note, else False."""
        self.ensure_one()
        j = self.journal_id
        try:
            if self.move_type == "out_invoice":
                if j.invoice_use_custom_title:
                    title = (j.invoice_custom_title or "").strip()
                    if not title:
                        _logger.warning(
                            "[s3_invoice_pdf_titles] Journal %s: invoice_use_custom_title enabled but invoice_custom_title empty",
                            j.display_name,
                        )
                        return False
                    return title

            if self.move_type == "out_refund":
                if j.credit_note_use_custom_title:
                    title = (j.credit_note_custom_title or "").strip()
                    if not title:
                        _logger.warning(
                            "[s3_invoice_pdf_titles] Journal %s: credit_note_use_custom_title enabled but credit_note_custom_title empty",
                            j.display_name,
                        )
                        return False
                    return title

        except Exception:
            _logger.exception("[s3_invoice_pdf_titles] _pdf_custom_title failed for move id=%s", self.id)
        return False