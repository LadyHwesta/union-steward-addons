# -*- coding: utf-8 -*-
from odoo import fields, models


class UnionContract(models.Model):
    """A collective bargaining agreement with one employer. Its bargaining
    units, and (with union_grievance) its grievance procedure, hang off it,
    so each union sets up its own contract's terms instead of them being
    written into the code."""
    _name = "union.contract"
    _description = "Collective Bargaining Agreement"
    _order = "date_start desc, name"

    name = fields.Char(required=True, help='e.g. "Memorial Hospital 2024-2028"')
    employer_id = fields.Many2one(
        "res.partner", string="Employer", required=True,
        domain=[("is_company", "=", True)])
    date_start = fields.Date(string="Effective From")
    date_end = fields.Date(string="Expires")
    unit_ids = fields.One2many("union.unit", "contract_id", string="Bargaining Units")
    shift_notes = fields.Text(
        string="Shifts and Differentials",
        help="The contract's shift times and differential pay, shown next to "
             "each member's shift.")
    notes = fields.Html()
    active = fields.Boolean(default=True)
