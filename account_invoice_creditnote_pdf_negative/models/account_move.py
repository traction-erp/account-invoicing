# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    def _pdf_refund_sign(self):
        """Return -1 only when:
        - the move is a refund (out_refund or in_refund)
        - AND the journal has refund_pdf_negative enabled
        Otherwise return 1.
        """
        self.ensure_one()
        try:
            enabled = bool(self.journal_id.refund_pdf_negative)
            is_refund = self.move_type in ("out_refund", "in_refund")
            sign = -1 if (enabled and is_refund) else 1

            # Proactive troubleshooting signal (only DEBUG to avoid log spam)
            _logger.debug(
                "[s3_creditnote_pdf_negative] move=%s type=%s journal=%s refund_pdf_negative=%s => sign=%s",
                self.id, self.move_type, self.journal_id.display_name, enabled, sign
            )
            return sign
        except Exception:
            _logger.exception("[s3_creditnote_pdf_negative] _pdf_refund_sign failed for move id=%s", self.id)
            return 1