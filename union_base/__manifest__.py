# -*- coding: utf-8 -*-
{
    "name": "Union Steward Suite - Base",
    "version": "19.0.2.0.0",
    "category": "Association",
    "summary": "Members, stewards, contracts and bargaining units for a union local",
    "description": """
Union Steward Suite - Base
==========================

The foundation of the steward suite, for any union local. Nothing here is
specific to one union or contract: a contract pack (such as
``union_contract_nuhw_srmh``) adds a real contract's details as data.

* **Contracts** - one record per collective bargaining agreement: the
  employer, its dates, its bargaining units, and its shift and
  differential terms. With ``union_grievance`` it also holds the
  contract's grievance procedure.
* **Members** - depends on OCA's ``membership`` module for its "Members"
  menu/action, distinct from core Customers. Dues usually come by payroll
  check-off rather than invoices, so a one-click **Mark Dues Current**
  records a year as paid without an invoice.
* **Bargaining units** - each belongs to a contract; a member's unit shows
  their contract, and their shift shows the contract's differentials. A
  free-text job classification holds their actual title.
* **Stewards** - a flag plus which unit(s) they represent and when the
  employer was told in writing, with a Stewards menu filtered to them.
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/union-steward-addons",
    "depends": ["membership", "contacts"],
    "data": [
        "security/union_security.xml",
        "security/ir.model.access.csv",
        "data/union_dues_data.xml",
        "views/union_contract_views.xml",
        "views/union_unit_views.xml",
        "views/res_partner_views.xml",
        "views/union_menus.xml",
    ],
    "installable": True,
    "application": True,
}
