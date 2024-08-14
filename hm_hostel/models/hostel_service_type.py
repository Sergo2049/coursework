from odoo import fields, models


class HostelServiceType(models.Model):

    _name = "hostel.service.type"
    _description = "Hostel Service Type"

    name = fields.Char(required=True, translate=True)

    is_available = fields.Boolean(default=True)

    price = fields.Monetary(currency_field='currency_id',
                            required=True,
                            help="""You can change currency in your company
                                  settings.""")

    currency_id = fields.Many2one('res.currency',
                                  'Currency',
                                  readonly=True,
                                  default=lambda
                                  self: self.env.company.currency_id)
