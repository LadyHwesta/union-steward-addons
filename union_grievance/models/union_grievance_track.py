# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields, models


class UnionGrievanceTrack(models.Model):
    """One grievance procedure in a contract, e.g. "Contract interpretation"
    or "Discipline and discharge": an ordered list of steps, each with its
    own deadline. Contracts often have more than one track."""
    _name = "union.grievance.track"
    _description = "Grievance Procedure"
    _order = "contract_id, sequence, id"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    contract_id = fields.Many2one(
        "union.contract", string="Contract", required=True, ondelete="cascade")
    article = fields.Char(
        string="Contract Article/Section",
        help='Where the contract sets out this procedure, e.g. "30.3".')
    filed_by = fields.Selection(
        [("union", "Union"), ("employer", "Employer")],
        default="union", required=True,
        help="Most procedures are for grievances the union files; some "
             "contracts also let the employer grieve against the union.")
    step_ids = fields.One2many(
        "union.grievance.step", "track_id", string="Steps", copy=True)
    notes = fields.Text(
        help="Anything else stewards should know, e.g. what missing a "
             "deadline means under this contract.")


class UnionGrievanceStep(models.Model):
    _name = "union.grievance.step"
    _description = "Grievance Procedure Step"
    _order = "track_id, sequence, id"

    track_id = fields.Many2one(
        "union.grievance.track", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True, help='e.g. "Step 2 - HR Manager"')
    deadline_days = fields.Integer(
        string="Days to Act",
        help="How long after the previous step (or the incident) this step "
             "must happen. 0 means the contract sets no fixed deadline.")
    day_kind = fields.Selection(
        [("calendar", "Calendar days"), ("business", "Business days")],
        default="calendar", required=True,
        help="How the contract counts days. Business days skip Saturdays "
             "and Sundays.")
    description = fields.Char(
        help="Who it goes to and what happens, in a few words.")

    def _deadline_from(self, start):
        """The date this step is due, counted from `start`; False when the
        contract sets no deadline for it."""
        self.ensure_one()
        if not start or not self.deadline_days:
            return False
        if self.day_kind == "calendar":
            return start + timedelta(days=self.deadline_days)
        day, left = start, self.deadline_days
        while left:
            day += timedelta(days=1)
            if day.weekday() < 5:
                left -= 1
        return day


class UnionContract(models.Model):
    _inherit = "union.contract"

    grievance_track_ids = fields.One2many(
        "union.grievance.track", "contract_id", string="Grievance Procedures")
