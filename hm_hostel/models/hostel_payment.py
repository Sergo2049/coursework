from odoo import fields, models


class HostelPayment(models.Model):

    _name = "hostel.payment"
    _description = "Hostel Payment"

    active = fields.Boolean(default=True)

    type = fields.Selection(selection=[('cash', 'Cash'),
                                       ('credit_card', 'Credit card')],
                            default='credit_card')

    booking_id = fields.Many2one('hostel.booking',
                                 required=True)

    amount = fields.Monetary(currency_field='currency_id',
                             required=True,
                             help="""You can change currency in your company
                                  settings.""")

    currency_id = fields.Many2one('res.currency',
                                  'Currency',
                                  readonly=True,
                                  default=lambda
                                  self: self.env.company.currency_id)
