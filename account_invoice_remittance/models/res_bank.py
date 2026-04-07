from odoo import fields, models


class ResBank(models.Model):
    _inherit = "res.bank"

    clearing_code = fields.Char(
        string="Bank / Clearing Code",
        help=(
            "Country-specific bank clearing or routing code "
            "(e.g. PL: 8-digit bank code, UK: sort code, US: routing number)."
        ),
    )
