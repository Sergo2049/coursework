# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HostelService(models.Model):
    _name = "hostel.service"
    _description = "Hostel Service"

    service_type_id = fields.Many2one('hostel.service.type',
                                      domain="[('is_available', '=', True)]",
                                      required=True)

    booking_id = fields.Many2one('hostel.booking',
                                 readonly=True)

    price = fields.Monetary(related="service_type_id.price",
                            currency_field='currency_id',
                            readonly=True,
                            store=True,
                            help="""You can change currency in your company
                                  settings.""")

    currency_id = fields.Many2one(related='service_type_id.currency_id',
                                  string='Currency', readonly=True)

    quantity = fields.Integer(required=True,
                              default=1)

    total_amount = fields.Monetary(currency_field='currency_id',
                             compute='_compute_total_amount',
                             readonly=True, store=True, string='Total')

    @api.depends('service_type_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec.service_type_id.name

    @api.depends('price','quantity')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.price * rec.quantity