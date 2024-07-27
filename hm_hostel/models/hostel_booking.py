# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError

class Hostel_booking(models.Model):

    _name = "hostel.booking"
    _description = "Hostel booking"

    start_date = fields.Date(default=fields.date.today(),
                                 required=True)

    end_date = fields.Date(default=fields.date.today() + timedelta(days=1),
                               required=True)

    booking_days = fields.Integer(compute='_compute_booking_days',
                                  string='Days')


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
    room_id = fields.Many2one(related='bed_id.room_id',
                              string='Room')

    room_price = fields.Monetary(string='Room Price')

    currency_id = fields.Many2one('res.currency', string='Currency')

    total_bed_price = fields.Monetary(currency_field='currency_id')

    service_ids = fields.One2many('hostel.service',
                                  'booking_id')

    @api.onchange('room_id')
    def get_room_price(self):
        for rec in self:
            if rec.room_id:
                rec.room_price = rec.room_id.price
                rec.currency_id = rec.room_id.currency_id.id
            else:
                rec.room_price = 0
                rec.currency_id = self.env.company.currency_id.id


    @api.depends('start_date', 'end_date')
    def _compute_booking_days(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.booking_days = (rec.end_date - rec.start_date).days
            else:
                rec.booking_days = 0

    @api.depends('visitor_id', 'start_date', 'end_date')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (f"{rec.visitor_id.display_name}:  "
                                f"{rec.start_date.strftime('%Y-%m-%d')} "
                                f"- {rec.end_date.strftime('%Y-%m-%d')}")

    @api.constrains('sta07/26/2024 03:00:00rt_date', 'end_date')
    def check_dates(self):
        """End booking date must be at least one day later the booking start
        date"""
        self.ensure_one()
        if self.end_date and self.start_date:
            if (self.end_date - self.start_date).days < 1:
                raise ValidationError(
                    _('Booking end date must be at least one day '
                      'later than booking start date.'))

#TODO: delete this action
    def action_test(self):
        print(self.roomroom_id.price)
    #TODO cant change visit status if payment exist
    #TODO gender booking room constrains
    #TODO compute sum for booking
    #TODO check if room aviable this day

