# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class Hostel_booking(models.Model):

    _name = "hostel.booking"
    _description = "Hostel booking"

    start_date = fields.Datetime(default=fields.date.today(),
                             required=True)

    end_date = fields.Datetime(default=fields.date.today(),
                           required=True)

    state = fields.Selection([('planned', 'Planned'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')],
                             default='planned')
    # TODO: Total payment - compute field based on price and duration
    # TODO: payment_ftate - compute, readonly

    visitor_id = fields.Many2one('hostel.visitor',
                                 required=True)
    bed_id = fields.Many2one('hostel.bed',
                                 required=True)
    service_ids = fields.One2many('hostel.service',
                                  'booking_id')

    # TODO:
    @api.depends('visitor_id', 'start_date', 'end_date')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (f"{rec.visitor_id.display_name}:  "
                                f"{rec.start_date.strftime('%Y-%m-%d')} "
                                f"- {rec.end_date.strftime('%Y-%m-%d')}")

    # TODO cant change visit status if payment exist
