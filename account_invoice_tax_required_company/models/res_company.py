from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    require_tax_on_invoices = fields.Boolean(
        string="Require taxes on invoices",
        help=(
            "When enabled, invoices and bills for this company cannot be "
            "posted if a normal invoice line has no taxes."
        ),
    )