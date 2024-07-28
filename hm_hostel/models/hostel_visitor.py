# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HostelVisitor(models.Model):

    _name = "hostel.visitor"
    _description = "Hostel Visitor"  # TODO

    first_name = fields.Char(required=True)

    last_name = fields.Char(required=True)

    display_name = fields.Char(compute='_compute_display_name', store=True,
                               index=True)

    phone = fields.Char(required=True,
                        index=True)

    passport_data = fields.Text()

    gender = fields.Selection(selection=[('male', 'Male'),
                               ('female', 'Female')],
                              required=True,
                              default='male'
                              )

    image_256 = fields.Image('image_256',
                             max_width=256, max_height=256)

    booking_ids = fields.One2many('hostel.booking',
                                  'visitor_id',
                                  readonly=True)

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.first_name} {rec.last_name}'

    @api.constrains('phone')
    def check_phone(self):
        """The phone number must be unique"""
        for rec in self:
            search = rec.search_count([('phone', '=', rec.phone),
                                       ('id', '!=', self.id)])
            if search > 0:
                raise ValidationError(_('A visitor with the specified number '
                                        'already exists'))