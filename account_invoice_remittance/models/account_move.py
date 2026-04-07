# s3_invoice_remittance/models/account_move.py
import re

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoice_remittance_data(self):
        self.ensure_one()
        j = self.journal_id

        # Always return {} when not enabled
        if not self._is_invoice_remittance_enabled():
            return {}

        # …your existing bank selection logic…
        partner_bank = self.partner_bank_id
        if not partner_bank:
            company_partner = self.company_id.partner_id
            bank_candidates = company_partner.bank_ids.filtered(
                lambda b: not b.company_id or b.company_id == self.company_id
            )
            partner_bank = bank_candidates[:1]
            partner_bank = partner_bank and partner_bank[0] or False

        bank = partner_bank.bank_id if partner_bank else False
        clearing_code = bank.clearing_code if bank and getattr(bank, "clearing_code", False) else ""

        iban = partner_bank.acc_number if partner_bank else ""

        # UK account number extraction: last 8 digits of the IBAN (digits only)
        account_no_8 = ""
        if iban:
            iban_digits = re.sub(r"\D", "", iban)
            if len(iban_digits) >= 8:
                account_no_8 = iban_digits[-8:]

        return {
            "mode": j.invoice_remittance_mode,  # <<< IMPORTANT
            "beneficiary_name": (partner_bank.partner_id.name if partner_bank else "") or self.company_id.name or "",
            "beneficiary_bank": bank.name if bank else "",
            "swift": bank.bic if bank and bank.bic else "",
            "clearing_code": clearing_code,
            "iban": iban,
            "account_no_8": account_no_8,  # <<< NEW
            "due_date": self.invoice_date_due,
        }

    def _is_invoice_remittance_enabled(self):
        self.ensure_one()
        j = self.journal_id
        return (
            self.move_type in ("out_invoice", "out_refund")
            and j.type == "sale"
            and j.invoice_remittance_mode
            and j.invoice_remittance_mode != "none"
        )
