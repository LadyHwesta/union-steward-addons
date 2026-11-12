# -*- coding: utf-8 -*-
from datetime import date

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestNuhwContract(TransactionCase):
    """The pack gives exactly the deadlines the suite had built in before it
    was made general (Article 30, calendar days)."""

    def _deadline(self, track_xmlid, step_name):
        track = self.env.ref(f"union_contract_nuhw_srmh.{track_xmlid}")
        member = self.env["res.partner"].create({
            "name": "Member",
            "bargaining_unit_id": self.env.ref("union_contract_nuhw_srmh.unit_service_technical").id})
        grievance = self.env["union.grievance"].create({
            "partner_id": member.id, "track_id": track.id,
            "step_id": track.step_ids.filtered(lambda s: s.name == step_name).id,
            "date_filed": date(2027, 1, 1)})
        grievance._onchange_deadline_suggestion()
        return grievance.response_deadline_date

    def test_article_30_deadlines(self):
        self.assertEqual(self._deadline("track_contract_interpretation", "Step 2 - HR Manager"), date(2027, 1, 22))
        self.assertEqual(self._deadline("track_contract_interpretation", "Step 3 - Area Director"), date(2027, 1, 21))
        self.assertEqual(self._deadline("track_discipline_discharge", "Step 1 - HR Manager"), date(2027, 1, 8))
        for track in ("track_contract_interpretation", "track_discipline_discharge"):
            self.assertEqual(self._deadline(track, "Arbitration"), date(2027, 1, 31))
        self.assertFalse(self._deadline("track_contract_interpretation", "Step 1 - Informal Review"))

    def test_contract_units_and_names(self):
        contract = self.env.ref("union_contract_nuhw_srmh.contract_srmh")
        self.assertEqual(contract.employer_id.name, "Santa Rosa Memorial Hospital")
        self.assertEqual(set(contract.unit_ids.mapped("code")), {"S&T", "PROF"})
        self.assertIn("25% of base hourly rate", contract.shift_notes)
        self.assertEqual(contract.release_notice_hours, 48)
        self.assertEqual(len(contract.grievance_track_ids), 3)
        hospital = self.env.ref("union_contract_nuhw_srmh.track_hospital_grievance")
        self.assertEqual(hospital.filed_by, "employer")
        dues = self.env.ref("union_base.product_template_union_dues")
        self.assertTrue(dues.name.startswith("NUHW Membership"))
