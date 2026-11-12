# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    bargaining_unit_id = fields.Many2one(
        "union.unit", string="Bargaining Unit",
        help="The unit this person belongs to under their contract's "
             "recognition clause.")
    union_contract_id = fields.Many2one(
        related="bargaining_unit_id.contract_id", string="Contract")
    job_classification = fields.Char(
        help="The person's actual job title or classification. Free text, "
             "since employers add and rename titles over time.")
    shift = fields.Selection(
        [("day", "Day"), ("evening", "Evening"), ("night", "Night")])
    contract_shift_notes = fields.Text(
        related="bargaining_unit_id.contract_id.shift_notes",
        string="Shifts and Differentials")
    hire_date = fields.Date(help="Used for seniority.")
    is_steward = fields.Boolean(string="Is a Union Steward")
    steward_unit_ids = fields.Many2many(
        "union.unit", string="Units Represented as Steward",
        help="Which bargaining unit(s) this person is designated to "
             "represent as steward. Defaults to their own unit.")
    steward_designated_date = fields.Date(
        help="When the employer was told, in writing, that this person is a "
             "steward. Most contracts require that notice.")

    @api.onchange("is_steward")
    def _onchange_is_steward_default_unit(self):
        for partner in self:
            if partner.is_steward and partner.bargaining_unit_id \
                    and partner.bargaining_unit_id not in partner.steward_unit_ids:
                partner.steward_unit_ids = [(4, partner.bargaining_unit_id.id)]

    def action_mark_dues_current(self):
        """Create/refresh one year of a 'paid' membership line without
        going through membership's invoice-driven renewal workflow. Dues
        are usually deducted by the employer's payroll (check-off), not
        invoiced through this database, so there's never an invoice to
        drive membership_state's own compute off of.
        """
        today = fields.Date.context_today(self)
        dues_product = self.env.ref(
            "union_base.product_template_union_dues").product_variant_id
        for partner in self:
            line = partner.member_line_ids.filtered(
                lambda line: not line.date_to or line.date_to >= today)[:1]
            values = {
                "partner_id": partner.id,
                "membership_id": dues_product.id,
                "member_price": dues_product.list_price,
                "date_from": today,
                "date_to": today + relativedelta(years=1),
                "state": "paid",
            }
            if line:
                line.write(values)
            else:
                self.env["membership.membership_line"].create(values)
