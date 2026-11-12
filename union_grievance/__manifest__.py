# -*- coding: utf-8 -*-
{
    "name": "Union Steward Suite - Grievances",
    "version": "19.0.2.0.0",
    "category": "Association",
    "summary": "Grievance tracking that follows each contract's own procedure and deadlines",
    "description": """
Union Steward Suite - Grievances
================================

A plain, domain-named grievance model instead of a generic ticket/helpdesk
framework, for any union and contract:

* **Grievance procedures are data, per contract.** Each contract has one or
  more procedures (e.g. contract interpretation, discipline and discharge,
  employer grievances), each an ordered list of steps with its own
  deadline in calendar or business days. Set them up under Union >
  Configuration > Grievance Procedures, or install a contract pack (such
  as ``union_contract_nuhw_srmh``) that already has them.
* A grievance picks its contract from the grievant's unit, then its
  procedure; its step starts at the first one, and **Next Step** moves on,
  dated today, with the deadline filled in. The deadline stays editable,
  since real deadlines key off actual meeting dates.
* Grievances filed by the **employer** against the union are covered by
  procedures marked as such.
* **Missed deadlines** have different consequences under different
  contracts; the outcome field covers dismissal, and the procedure's notes
  say what applies.
* A native Odoo activity gets scheduled against the deadline on the
  assigned steward's user whenever it's set or changes - no custom cron,
  just ``mail.activity.mixin``.
* Optionally links back to one or more Weingarten meetings that led to it
  (``union_weingarten`` stays fully standalone - this module owns the link
  by adding the ``grievance_id`` field onto that model).
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/union-steward-addons",
    "depends": ["union_weingarten"],
    "data": [
        "security/ir.model.access.csv",
        "views/union_grievance_track_views.xml",
        "views/union_grievance_views.xml",
        "views/union_weingarten_meeting_views.xml",
        "views/union_menus.xml",
    ],
    "installable": True,
    "application": False,
}
