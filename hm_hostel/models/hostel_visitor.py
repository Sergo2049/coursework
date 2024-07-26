# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class HostelVisitor(models.Model):

    _name = "hostel.visitor"
    _description = "Hostel Visitor"  # TODO

    first_name = fields.Char(required=True)

    last_name = fields.Char(required=True)

    phone = fields.Char(required=True)

    passport_data = fields.Text()

    gender = fields.Selection(selection=[('male', 'Male'),
                               ('female', 'Female')],
                              required=True,
                              default='male'
                              )
    # image = fields.Image('image', max_width=1920, max_height=1920)
    # image_256 = fields.Image('image_256', related='image',
    #                          max_width=256, max_height=256)
    image_256 = fields.Image('image_256',
                             max_width=256, max_height=256)

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.first_name} {rec.last_name}'