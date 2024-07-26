# Copyright 2024 Sergii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HostelBed(models.Model):

    _name = "hostel.bed"

    _description = "Hostel Bed"  # TODO

    name = fields.Char(string='Bed',
                       required=True,
                       help='Bed number')

    room_id = fields.Many2one(comodel_name='hostel.room',
                              required=True)

    @api.depends()
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.room_id.name}-{rec.name}'
