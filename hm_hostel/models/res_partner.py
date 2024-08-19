from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):

    _inherit = 'res.partner'

    passport_data = fields.Text(string='Passport data')

    gender = fields.Selection(selection=[('male', 'Male'),
                                         ('female', 'Female')],
                              required=True,
                              default='male'
                              )

    booking_ids = fields.One2many('hostel.booking',
                                  'visitor_id',
                                  readonly=True)

    @api.constrains('mobile')
    def _check_mobile(self):
        """The phone number must be unique"""
        for rec in self:
            search = rec.search_count([('mobile', '=', rec.mobile),
                                       ('id', '!=', self.id)])
            if search > 0:
                raise ValidationError(_('A visitor with the specified number '
                                        'already exists'))
