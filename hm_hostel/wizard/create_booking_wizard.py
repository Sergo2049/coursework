from odoo import fields, models
from datetime import timedelta
class CreateBookingWizard(models.TransientModel):
    _name = 'create.booking.wizard'
    _description = 'Create Booking Wizard'

    planned_start_date = fields.Date(required=True,
                                     default=fields.Date.today())

    planned_end_date = fields.Date(required=True,
                                   default=fields.Date.today()
                                           + timedelta(days=1))

    visitor_id = fields.Many2one('hostel.visitor', required=True,
                                 string='Visitor')

    bed_id = fields.Many2one('hostel.bed', required=True,
                             string='Bed')

    room_id = fields.Many2one(related='bed_id.room_id', readonly=True,
                              string='Room')

    def get_available_beds(self):
        return