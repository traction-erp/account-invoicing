{
    "name": "Account Invoice Tax Required Company",
    "summary": "Configure required invoice taxes per company",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "TractionCRM - ERP-FTW",
    "website": "https://github.com/OCA/account-invoicing",
    "category": "Accounting/Accounting",
    "depends": [
        "account",
        "account_invoice_tax_required",
    ],
    "data": [
        "views/res_company_views.xml",
    ],
    "installable": True,
    "application": False,
}
