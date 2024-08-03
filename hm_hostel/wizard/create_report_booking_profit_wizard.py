from odoo import api, fields, models

class CreateReportBookingProfitWizard(models.TransientModel):
    _name = 'create.report.booking.profit.wizard'
    _description = 'Creates report of booking pfofit wizard'

    start_date = fields.Date(fields.Date.today().strftime('%Y-%m-01'))
    #TODO: get the end of the month
    end_date = fields.Date(fields.Date.today().strftime('%Y-%m-30'))

