from odoo import fields, models


class ResUser(models.Model):
    _inherit = 'res.users'

    birth_date = fields.Date()
