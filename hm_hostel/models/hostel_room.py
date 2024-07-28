# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HostelRoom(models.Model):

    _name = 'hostel.room'
    _description = 'Hostel Room'

    name = fields.Char(string='Room',
                       required=True,
                       help='Room number')

    active = fields.Boolean(default=True)

    type = fields.Selection([('shared', 'Shared'),
                                       ('private', 'Private')
                                       ],
                            default='shared',
                            required=True)
    price = fields.Monetary(currency_field='currency_id',
                            help="""You can change currency in your company
                                  settings.""")
    currency_id = fields.Many2one('res.currency',
                                  'Currency',
                                  readonly=True,
                                  default=lambda self: self.env.company.currency_id)

    bed_ids = fields.One2many(comodel_name='hostel.bed',
                              inverse_name='room_id',
                              readonly=True)

    def action_book(self):
        return

    # TODO: state
