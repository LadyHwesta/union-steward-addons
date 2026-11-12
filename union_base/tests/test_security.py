# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestUnionSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.unit = cls.env["union.unit"].create({
            "name": "Service and Technical Unit",
            "contract_id": cls.env["union.contract"].create({
                "name": "Test Contract",
                "employer_id": cls.env["res.partner"].create(
                    {"name": "Test Employer", "is_company": True}).id,
            }).id,
        })
        cls.plain_internal_user = cls.env["res.users"].create({
            "name": "Front Desk (no steward access)", "login": "union_front_desk",
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id])],
        })

    def test_plain_internal_user_can_read_units(self):
        self.unit.with_user(self.plain_internal_user).name

    def test_plain_internal_user_cannot_write_units(self):
        with self.assertRaises(AccessError):
            self.unit.with_user(self.plain_internal_user).write(
                {"name": "Renamed"})

    def test_plain_internal_user_cannot_create_units(self):
        with self.assertRaises(AccessError):
            self.env["union.unit"].with_user(
                self.plain_internal_user).create({"name": "New Unit"})
