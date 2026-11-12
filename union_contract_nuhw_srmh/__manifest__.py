# -*- coding: utf-8 -*-
{
    "name": "Union Contract: NUHW - Santa Rosa Memorial Hospital",
    "version": "19.0.1.0.0",
    "category": "Association",
    "summary": "The NUHW / Santa Rosa Memorial Hospital contract: units, "
               "shift differentials and grievance procedures (Article 30)",
    "description": """
NUHW - Santa Rosa Memorial Hospital contract pack
=================================================

Data only, on top of the Union Steward Suite: installs the collective
bargaining agreement between NUHW and Santa Rosa Memorial Hospital as it
was used to build the suite.

* Employer and contract, with the shift differential zones (Article 12.5).
* The two bargaining units (Article 2): Service and Technical, and
  Professionals (with the classifications in 2.4).
* Grievance procedures (Article 30, calendar days per 30.1):
  - Contract interpretation (30.3): Step 1 informal review, Step 2 HR
    Manager within 21 days, Step 3 Area Director within 20 days,
    arbitration within 30 days.
  - Discipline and discharge (30.4): HR Manager within 7 days, Area
    Director within 7 days, arbitration within 30 days (no Step 3).
  - Hospital grievances (30.5), filed by the employer, starting at the
    Area Director.
* Names the dues product "NUHW Membership".

Everything is ordinary data (installed once, not reset by upgrades), so
it can be edited when the contract is renegotiated.
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/union-steward-addons",
    "depends": ["union_grievance"],
    "data": ["data/nuhw_srmh_contract.xml"],
    "installable": True,
    "application": False,
}
