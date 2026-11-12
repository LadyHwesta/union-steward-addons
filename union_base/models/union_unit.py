# -*- coding: utf-8 -*-
from odoo import fields, models


class UnionUnit(models.Model):
    _name = "union.unit"
    _description = "Bargaining Unit"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(help="Short code, e.g. the unit abbreviation used on "
                            "grievance forms.")
    description = fields.Text()
    contract_id = fields.Many2one(
        "union.contract", string="Contract", ondelete="restrict",
        help="The collective bargaining agreement covering this unit.")
    member_ids = fields.One2many(
        "res.partner", "bargaining_unit_id", string="Members")
    member_count = fields.Integer(compute="_compute_member_count")

    def _compute_member_count(self):
        for unit in self:
            unit.member_count = len(unit.member_ids)
