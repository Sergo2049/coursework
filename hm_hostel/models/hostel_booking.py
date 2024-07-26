# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class Hostel_booking(models.Model):

    _name = "hostel_booking"
    _description = "Hostel booking"

    start_date = fields.Date()

    end_date = fields.Date()

    state = fields.Selection([('planned', 'Planned'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')])

    visitor_id = fields.Many2one()

    #TODO
    # @api.depends()
    # def _compute_display_name(self):
    #     for rec in self:
    #         rec.display_name = _____________________

    #TODO cant change visit status if payment exist