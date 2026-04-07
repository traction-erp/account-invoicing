# -*- coding: utf-8 -*-
import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)

class AccountJournal(models.Model):
    _inherit = "account.journal"

    refund_pdf_negative = fields.Boolean(string="Credit Notes Negative on PDF")