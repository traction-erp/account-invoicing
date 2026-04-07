from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _tax_required_applies(self):
        self.ensure_one()
        return bool(self.company_id.require_tax_on_invoices)

    def _test_invoice_line_tax(self):
        moves_to_check = self.filtered(lambda move: move._tax_required_applies())
        if not moves_to_check:
            return
        return super(AccountMove, moves_to_check)._test_invoice_line_tax()