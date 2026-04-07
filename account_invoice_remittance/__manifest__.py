# s3_invoice_remittance/__manifest__.py
{
    "name": "S3 Invoice Remittance Block",
    "version": "18.0.2.0.13",
    "summary": "Adds a generic remittance/payment instruction block to customer invoices. Options for clearing code and IBAN.",
    "author": "TractionCRM - ERP-FTW",
    "depends": [
        "account",
    ],
    "data": [
        "views/report_invoice_remittance.xml",
        "views/journal_form_view.xml",
        "views/bank_view.xml",

    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
