# -*- coding: utf-8 -*-
{
    "name": "Union Steward Suite - Direct Actions",
    "version": "19.0.2.0.0",
    "category": "Association",
    "summary": "Track informational pickets, rallies, petitions, and other "
               "direct actions",
    "description": """
Union Steward Suite - Direct Actions
=====================================

Lightweight tracking for organizing activity that isn't a grievance or a
Weingarten meeting - informational pickets, rallies, petition drives,
button days, know-your-rights trainings, and similar.
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/union-steward-addons",
    "depends": ["union_base"],
    "data": [
        "security/ir.model.access.csv",
        "views/union_direct_action_views.xml",
        "views/union_menus.xml",
    ],
    "installable": True,
    "application": False,
}
