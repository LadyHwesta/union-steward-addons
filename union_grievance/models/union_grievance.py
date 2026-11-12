# -*- coding: utf-8 -*-

from odoo import api, fields, models

class UnionGrievance(models.Model):
    _name = "union.grievance"
    _description = "Union Grievance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_filed desc"

    partner_id = fields.Many2one(
        "res.partner", string="Grievant", required=True, tracking=True)
    steward_id = fields.Many2one(
        "res.partner", string="Handling Steward",
        domain=[("is_steward", "=", True)], tracking=True)
    unit_id = fields.Many2one("union.unit", string="Unit")
    contract_id = fields.Many2one(
        "union.contract", string="Contract", tracking=True,
        help="Filled in from the unit; picks which grievance procedures apply.")
    track_id = fields.Many2one(
        "union.grievance.track", string="Procedure", required=True, tracking=True,
        domain="[('contract_id', '=', contract_id)]",
        help="Which of the contract's grievance procedures this follows, "
             "e.g. contract interpretation or discipline.")
    filed_by = fields.Selection(related="track_id.filed_by", store=True)
    incident_date = fields.Date()
    step_id = fields.Many2one(
        "union.grievance.step", string="Step", tracking=True,
        domain="[('track_id', '=', track_id)]",
        help="Where the grievance is in its procedure. Next Step moves it on "
             "and sets the next deadline.")
    date_filed = fields.Date(
        string="Date of Current Step",
        default=fields.Date.context_today,
        help="When the current step's filing/meeting happened - the "
             "response_deadline_date default is computed from this date.")
    response_deadline_date = fields.Date(
        tracking=True,
        help="Filled in from the step's deadline in the contract, counted "
             "from the date of the current step. Stays editable, since real "
             "deadlines key off actual meeting dates.")
    description = fields.Text()
    cba_article = fields.Char(
        string="Contract Article/Section",
        help="Which Article/section is alleged to have been violated, "
             "e.g. \"12.5\".")
    weingarten_meeting_ids = fields.One2many(
        "union.weingarten_meeting", "grievance_id",
        string="Related Weingarten Meetings")
    outcome = fields.Selection(
        [("pending", "Pending"),
         ("granted", "Granted"),
         ("denied", "Denied"),
         ("settled", "Settled"),
         ("withdrawn", "Withdrawn"),
         ("dismissed_missed_deadline", "Dismissed - Missed Deadline")],
        default="pending", tracking=True,
        help="Contracts differ on missed deadlines: often a grievance the "
             "union lets lapse is dismissed, while the employer missing its "
             "response moves the grievance to the next step (use Next Step "
             "for that). See the procedure's notes.")
    notes = fields.Text()
    state = fields.Selection(
        [("open", "Open"), ("closed", "Closed")],
        default="open", tracking=True)
    is_overdue = fields.Boolean(
        compute="_compute_is_overdue",
        help="The response deadline has passed and the grievance is still "
             "open. Computed live (not stored) since it depends on "
             "today's date, not just this record's own fields - a search "
             "filter for this uses a plain date comparison instead (see "
             "the search view), which stays correct as days pass.")

    @api.depends("response_deadline_date", "state")
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for grievance in self:
            grievance.is_overdue = bool(
                grievance.response_deadline_date
                and grievance.response_deadline_date < today
                and grievance.state == "open")

    @api.onchange("step_id", "date_filed")
    def _onchange_deadline_suggestion(self):
        for grievance in self:
            deadline = grievance.step_id._deadline_from(grievance.date_filed)
            if deadline:
                grievance.response_deadline_date = deadline

    @api.onchange("track_id")
    def _onchange_track_first_step(self):
        for grievance in self:
            if grievance.step_id.track_id != grievance.track_id:
                grievance.step_id = grievance.track_id.step_ids[:1]

    def action_next_step(self):
        """Move on to the procedure's next step, dated today, with its
        deadline filled in."""
        today = fields.Date.context_today(self)
        for grievance in self:
            steps = grievance.track_id.step_ids
            later = steps.filtered(lambda s: (s.sequence, s.id) > (
                grievance.step_id.sequence, grievance.step_id.id)) if grievance.step_id else steps
            if not later:
                continue
            step = later[0]
            grievance.write({
                "step_id": step.id,
                "date_filed": today,
                "response_deadline_date": step._deadline_from(today),
            })

    @api.onchange("partner_id")
    def _onchange_partner_id_default_unit(self):
        for grievance in self:
            if grievance.partner_id.bargaining_unit_id:
                grievance.unit_id = grievance.partner_id.bargaining_unit_id
                grievance.contract_id = grievance.unit_id.contract_id

    def _activity_user_id(self):
        self.ensure_one()
        return self.steward_id.user_ids[:1].id or self.env.user.id

    def _sync_deadline_activity(self):
        activity_type = self.env.ref("mail.mail_activity_data_todo")
        for grievance in self:
            existing = grievance.activity_ids.filtered(
                lambda act: act.activity_type_id == activity_type)
            if not grievance.response_deadline_date \
                    or grievance.state == "closed":
                existing.unlink()
                continue
            if existing:
                existing.write({
                    "date_deadline": grievance.response_deadline_date,
                    "user_id": grievance._activity_user_id(),
                })
            else:
                grievance.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=grievance.response_deadline_date,
                    user_id=grievance._activity_user_id(),
                    summary="Grievance deadline",
                    note=f"Next action due for grievance "
                         f"\"{grievance.display_name}\".")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            track = self.env["union.grievance.track"].browse(vals.get("track_id"))
            if track and not vals.get("contract_id"):
                vals["contract_id"] = track.contract_id.id
            if track and not vals.get("step_id") and track.step_ids:
                vals["step_id"] = track.step_ids[0].id
        grievances = super().create(vals_list)
        grievances._sync_deadline_activity()
        return grievances

    def write(self, vals):
        result = super().write(vals)
        if {"response_deadline_date", "steward_id", "state"} & set(vals):
            self._sync_deadline_activity()
        return result
