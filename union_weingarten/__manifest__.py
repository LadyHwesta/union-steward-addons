# -*- coding: utf-8 -*-
{
    "name": "Union Steward Suite - Weingarten Meetings",
    "version": "19.0.2.0.0",
    "category": "Association",
    "summary": "Track investigatory interviews and steward representation "
               "requests (Weingarten rights)",
    "description": """
Union Steward Suite - Weingarten Meetings
=========================================

A Weingarten meeting is an employee's right to union representation during
an investigatory interview that could lead to discipline. Not every one of
these leads to a grievance, and a grievance can exist without one, so this
is its own standalone model - optionally linked to a grievance once
``union_grievance`` is installed.

* Who's being interviewed, which steward(s) are representing them, the
  employer's own representative, the unit, and a dedicated notes field
  (alongside chatter) for what actually happened.
* Each contract can set a **steward release notice** in hours; a meeting
  whose release was requested later than that is flagged, since a late
  request is a contractual fact worth surfacing, not just a courtesy.
""",
    "author": "Tiesa",
    "license": "LGPL-3",
    "website": "https://github.com/LadyHwesta/union-steward-addons",
    "depends": ["union_base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/union_weingarten_meeting_views.xml",
        "views/union_menus.xml",
    ],
    "installable": True,
    "application": False,
}
