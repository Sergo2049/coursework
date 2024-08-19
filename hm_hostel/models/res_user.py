from dateutil import relativedelta
from datetime import date
from odoo import api, fields, models


class ResUser(models.Model):
    _inherit = 'res.users'

    birth_date = fields.Date()
