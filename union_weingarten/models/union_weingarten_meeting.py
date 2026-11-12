# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models



class UnionContract(models.Model):
    _inherit = "union.contract"

    release_notice_hours = fields.Integer(
        string="Steward Release Notice (hours)",
        help="How far ahead a steward must ask to be released for a meeting "
             "under this contract (often the same notice the employer owes "
             "for an investigatory interview). 0: no rule, nothing flagged.")


class UnionWeingartenMeeting(models.Model):
    _name = "union.weingarten_meeting"
    _description = "Union Weingarten Meeting"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "scheduled_date desc"

    partner_id = fields.Many2one(
        "res.partner", string="Employee", required=True, tracking=True,
        help="The employee being interviewed.")
    steward_ids = fields.Many2many(
        "res.partner", string="Steward(s) Representing",
        domain=[("is_steward", "=", True)], tracking=True)
    management_rep = fields.Char(
        string="Management Representative(s)",
        help="Name/title of whoever from management is present - "
             "not tracked as a partner since management reps aren't union "
             "members.")
    unit_id = fields.Many2one("union.unit", string="Unit")
    subject = fields.Char(help="Reason for the interview.")
    request_date = fields.Datetime(
        string="Release Requested On",
        help="When the steward's release was requested. The contract may "
             "require a minimum notice; see release_notice_hours.")
    scheduled_date = fields.Datetime(tracking=True)
    release_notice_hours = fields.Integer(
        related="unit_id.contract_id.release_notice_hours")
    release_requested_late = fields.Boolean(
        compute="_compute_release_requested_late", store=True,
        help="True if the release request came later than the contract's "
             "required notice before the scheduled meeting.")
    location = fields.Char()
    state = fields.Selection(
        [("requested", "Requested"),
         ("scheduled", "Scheduled"),
         ("completed", "Completed"),
         ("rescheduled", "Rescheduled"),
         ("cancelled", "Cancelled")],
        default="requested", tracking=True)
    notes = fields.Text(help="What actually happened - in addition to the "
                              "chatter log above, for a longer write-up.")

    @api.depends("request_date", "scheduled_date", "unit_id.contract_id.release_notice_hours")
    def _compute_release_requested_late(self):
        for meeting in self:
            hours = meeting.unit_id.contract_id.release_notice_hours
            if hours and meeting.request_date and meeting.scheduled_date:
                notice = meeting.scheduled_date - meeting.request_date
                meeting.release_requested_late = notice < timedelta(hours=hours)
            else:
                meeting.release_requested_late = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("unit_id") and vals.get("partner_id"):
                partner = self.env["res.partner"].browse(vals["partner_id"])
                vals["unit_id"] = partner.bargaining_unit_id.id
        return super().create(vals_list)

    @api.onchange("partner_id")
    def _onchange_partner_id_default_unit(self):
        for meeting in self:
            if meeting.partner_id.bargaining_unit_id:
                meeting.unit_id = meeting.partner_id.bargaining_unit_id
