# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    union_hardship_disbursement_account_id = fields.Many2one(
        related="company_id.union_hardship_disbursement_account_id",
        readonly=False)
    union_hardship_payable_account_id = fields.Many2one(
        related="company_id.union_hardship_payable_account_id",
        readonly=False)
