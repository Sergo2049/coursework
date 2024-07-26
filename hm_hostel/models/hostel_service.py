# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HostelService(models.Model):

    _name = "hostel.service"
    _description = "Hostel Service"  # TODO

    name = fields.Char()
    # price = fields.Monetary(currency_field='company_currency')
