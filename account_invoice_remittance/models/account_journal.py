# s3_invoice_remittance/models/account_journal.py
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    invoice_remittance_mode = fields.Selection(
        [
            ("none", "No remittance block"),
            ("with_clearing", "Remittance block (with clearing code)"),
            ("without_clearing", "Remittance block (without clearing code)"),
            ("uk_with_account_no", "Remittance block (UK: show sort code + account no from IBAN)"),
        ],
        string="Invoice Remittance",
        default="none",
        help="Controls whether invoices from this journal print a remittance block and whether the clearing code is shown.",
    )
