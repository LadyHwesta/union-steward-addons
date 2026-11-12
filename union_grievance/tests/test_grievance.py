# -*- coding: utf-8 -*-
from datetime import date

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestGrievance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        employer = cls.env["res.partner"].create({"name": "Test Employer", "is_company": True})
        cls.contract = cls.env["union.contract"].create({
            "name": "Test Contract", "employer_id": employer.id})
        cls.unit = cls.env["union.unit"].create({
            "name": "Test Unit", "contract_id": cls.contract.id})

        def track(name, steps, **extra):
            return cls.env["union.grievance.track"].create(dict({
                "name": name, "contract_id": cls.contract.id,
                "step_ids": [(0, 0, {"name": n, "sequence": i, "deadline_days": d,
                                     "day_kind": kind})
                             for i, (n, d, kind) in enumerate(steps)],
            }, **extra))

        cls.interpretation = track("Contract interpretation", [
            ("Informal", 0, "calendar"), ("HR Manager", 21, "calendar"),
            ("Director", 20, "calendar"), ("Arbitration", 30, "calendar")])
        cls.business = track("Business-day procedure", [("Supervisor", 5, "business")])
        cls.grievant = cls.env["res.partner"].create({
            "name": "Jamie Chen", "bargaining_unit_id": cls.unit.id,
        })
        cls.steward = cls.env["res.partner"].create({"name": "Alex Rivera"})
        cls.steward_user = cls.env["res.users"].create({
            "name": "Alex Rivera", "login": "alex_rivera_steward",
            "partner_id": cls.steward.id,
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id,
                                   cls.env.ref("union_base.group_union_steward").id])],
        })

    def _step(self, track, name):
        return track.step_ids.filtered(lambda s: s.name == name)

    def _create_grievance(self, **kwargs):
        values = {
            "partner_id": self.grievant.id,
            "steward_id": self.steward.id,
            "track_id": self.interpretation.id,
            "date_filed": date(2027, 1, 1),
        }
        values.update(kwargs)
        return self.env["union.grievance"].create(values)

    def test_new_grievance_starts_at_the_first_step_of_its_contract(self):
        grievance = self._create_grievance()
        self.assertEqual(grievance.step_id, self._step(self.interpretation, "Informal"))
        self.assertEqual(grievance.contract_id, self.contract)
        self.assertEqual(grievance.filed_by, "union")

    def test_deadline_comes_from_the_steps_days(self):
        grievance = self._create_grievance(
            step_id=self._step(self.interpretation, "HR Manager").id)
        grievance._onchange_deadline_suggestion()
        self.assertEqual(grievance.response_deadline_date, date(2027, 1, 22))

    def test_a_step_without_a_deadline_sets_none(self):
        grievance = self._create_grievance()
        grievance._onchange_deadline_suggestion()
        self.assertFalse(grievance.response_deadline_date)

    def test_business_days_skip_weekends(self):
        # Friday 2027-01-01 + 5 business days = Friday 2027-01-08
        grievance = self._create_grievance(track_id=self.business.id)
        grievance._onchange_deadline_suggestion()
        self.assertEqual(grievance.response_deadline_date, date(2027, 1, 8))

    def test_next_step_moves_on_with_todays_deadline(self):
        grievance = self._create_grievance()
        grievance.action_next_step()
        self.assertEqual(grievance.step_id, self._step(self.interpretation, "HR Manager"))
        self.assertEqual(grievance.date_filed, date.today())
        self.assertEqual((grievance.response_deadline_date - date.today()).days, 21)
        grievance.step_id = self._step(self.interpretation, "Arbitration")
        grievance.action_next_step()
        self.assertEqual(grievance.step_id.name, "Arbitration", "nothing after the last step")

    def test_picking_the_grievants_unit_picks_the_contract(self):
        grievance = self.env["union.grievance"].new({"partner_id": self.grievant.id})
        grievance._onchange_partner_id_default_unit()
        self.assertEqual(grievance.contract_id, self.contract)

    def test_is_overdue_when_deadline_passed_and_open(self):
        grievance = self._create_grievance(response_deadline_date=date(2000, 1, 1))
        self.assertTrue(grievance.is_overdue)

    def test_is_overdue_false_once_closed(self):
        grievance = self._create_grievance(
            response_deadline_date=date(2000, 1, 1), state="closed")
        self.assertFalse(grievance.is_overdue)

    def test_create_schedules_a_deadline_activity_on_the_steward(self):
        grievance = self._create_grievance(response_deadline_date=date(2027, 2, 1))
        todo = self.env.ref("mail.mail_activity_data_todo")
        activities = grievance.activity_ids.filtered(lambda act: act.activity_type_id == todo)
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities.date_deadline, date(2027, 2, 1))
        self.assertEqual(activities.user_id, self.steward_user)

    def test_closing_the_grievance_removes_the_deadline_activity(self):
        grievance = self._create_grievance(response_deadline_date=date(2027, 2, 1))
        grievance.write({"state": "closed"})
        todo = self.env.ref("mail.mail_activity_data_todo")
        self.assertFalse(grievance.activity_ids.filtered(lambda act: act.activity_type_id == todo))

    def test_weingarten_meeting_links_back_to_grievance(self):
        grievance = self._create_grievance()
        meeting = self.env["union.weingarten_meeting"].create({
            "partner_id": self.grievant.id, "grievance_id": grievance.id,
        })
        self.assertIn(meeting, grievance.weingarten_meeting_ids)
