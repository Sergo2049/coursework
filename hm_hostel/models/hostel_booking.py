from odoo import _, api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError

class HostelBooking(models.Model):

    _name = "hostel.booking"
    _description = "Hostel booking"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(default=True)

    display_name = fields.Char(compute='_compute_display_name',
                           string='Booking')

    start_date = fields.Date(default=fields.date.today(),
                             required=True, tracking=True)

    end_date = fields.Date(default=fields.date.today() + timedelta(days=1),
                           required=True, tracking=True)

    booking_days = fields.Integer(compute='_compute_booking_days',
                                  string='Days')

    state = fields.Selection([('planned', _('Planned')),
                              ('confirmed', _('Confirmed')),
                              ('canceled', _('Canceled'))],
                             default='planned',
                             tracking=True)

    visitor_id = fields.Many2one('hostel.visitor',
                                 required=True, tracking=True)

    bed_id = fields.Many2one('hostel.bed',
                             required=True, tracking=True,
                             domain="[('id', 'in', available_bed_ids)]")

    room_id = fields.Many2one(related='bed_id.room_id',
                              string='Room',
                              store=True)

    room_price = fields.Monetary(compute='_compute_room_price',
                                 string='Room Price',
                                 store=True)

    currency_id = fields.Many2one('res.currency', string='Currency',
                                  readonly=True)

    total_bed_amount = fields.Monetary(compute='_compute_total_bed_amount',
                                       currency_field='currency_id',
                                       store=True)

    service_ids = fields.One2many('hostel.service',
                                  'booking_id',
                                  tracking=True)
    payment_ids = fields.One2many('hostel.payment',
                                  inverse_name='booking_id',
                                  tracking=True)

    service_total_amount = fields.Monetary(compute='_compute_total_amount',
                                           currency_field='currency_id',
                                           store=True, string='Service total',
                                           readonly=True)

    payment_total_amount = fields.Monetary(compute='_compute_payment_total_amount',
                                           currency_field='currency_id',
                                           store=True, string='Payment total',
                                           readonly=True)

    total_amount = fields.Monetary(compute='_compute_total_amount',
                                   currency_field='currency_id',
                                   store=True, readonly=True,
                                   string='Total')

    is_paid = fields.Boolean(compute='_compute_is_paid',
                             string='Paid')

    available_bed_ids = fields.Binary(compute='_compute_available_beds')

    @api.depends('room_id')
    def _compute_room_price(self):
        for rec in self:
            if rec.room_id:
                rec.room_price = rec.room_id.price
                rec.currency_id = rec.room_id.currency_id.id
            else:
                rec.room_price = 0
                rec.currency_id = self.env.company.currency_id.id

    @api.depends('room_price', 'booking_days')
    def _compute_total_bed_amount(self):
        for rec in self:
            rec.total_bed_amount = rec.room_price * rec.booking_days

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
    @api.depends('start_date', 'end_date', 'bed_id', 'service_ids')
    def _compute_total_amount(self):
        for rec in self:
            rec.service_total_amount = sum(service.total_amount
                                           for service in rec.service_ids)
            rec.total_amount = rec.total_bed_amount + rec.service_total_amount

    @api.depends('payment_ids')
    def _compute_payment_total_amount(self):
        for rec in self:
            rec.payment_total_amount = sum(payment.amount
                                           for payment in rec.payment_ids)

    @api.depends('total_amount', 'payment_ids')
    def _compute_is_paid(self):
        for rec in self:
            rec.is_paid = rec.payment_total_amount >= rec.total_amount

    @api.depends('start_date', 'end_date')
    def _compute_available_beds(self):
        self.ensure_one()
        if self.start_date and self.end_date:

            domain = [('state', '!=', 'canceled'),
                      ('start_date', '<=', self.end_date),
                      ('end_date', '>=', self.start_date)]
            if self.id:
                domain.append(('id', '!=', self.id))
            booked_beds = self.env['hostel.booking'].search(domain)

            booked_beds = booked_beds.mapped('bed_id.id')
            all_beds = self.env['hostel.bed'].search([]).ids
            available_beds = list(set(all_beds) - set(booked_beds))
            self.available_bed_ids = available_beds
        else:
            self.available_bed_ids = []
    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        """End booking date must be at least one day later the booking start
        date"""
        self.ensure_one()
        if self.end_date and self.start_date:
            if (self.end_date - self.start_date).days < 1:
                raise ValidationError(
                    _('Booking end date must be at least one day '
                      'later than booking start date.'))

    def check_is_room_available(self):
        """Check if the selected bed is available."""
        self.ensure_one()
        if self.bed_id.id not in self.available_bed_ids:
            raise ValidationError('The selected bed is not available for the specified dates.')

    @api.model
    def create(self, vals):
        """Check if the selected bed is available."""
        record = super(HostelBooking, self).create(vals)
        record.check_is_room_available()
        return record

    def write(self, vals):
        """Check if the selected bed is available."""
        res = super(HostelBooking, self).write(vals)
        self.check_is_room_available()
        return res

