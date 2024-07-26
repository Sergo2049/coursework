# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HostelServiceType(models.Model):

    _name = "hostel.service.type"
    _description = "Hostel Service Type"  # TODO

    name = fields.Char(required=True)
    state = fields.Selection([('available', 'Available'),
                              ('notavailable', 'Not available')],
                             default='available')
    price = fields.Monetary(currency_field='currency_id',
                            required=True,
                            help="""You can change currency in your company
                                  settings.""")
    currency_id = fields.Many2one('res.currency',
                                  'Currency',
                                  readonly=True,
                                  default=lambda
                                      self: self.env.company.currency_id)
