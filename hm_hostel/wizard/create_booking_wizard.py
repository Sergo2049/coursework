from odoo import api, fields, models
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

    @api.onchange('planned_start_date', 'planned_end_date')
    def _onchange_dates(self):
        if self.planned_start_date and self.planned_end_date:
            available_beds = self.get_available_beds()
            return {'domain': {'bed_id': [('id', '!in', available_beds)]}}

    def get_booked_beds(self):
        self.ensure_one()
        booked_beds = self.env['hostel.booking'].search(['&',('start_date','>=', self.planned_start_date), ('start_date',  '<=', self.planned_end_date), '&', ('end_date', '>=', self.planned_start_date),('end_date', '<=', self.planned_end_date)])
        booked_beds_ids = booked_beds.mapped('id')
        print(booked_beds)
        return booked_beds_ids

    def action_create_booking(self):
        booking_vals = {
            'start_date': self.planned_start_date,
            'end_date': self.planned_end_date,
            'visitor_id': self.visitor_id.id,
            'bed_id': self.bed_id.id,
            'state': 'planned',
        }
        new_booking = self.env['hostel.booking'].create(booking_vals)
        # return {'type': 'ir.actions.act_window_close'}

        return {
            'name': 'New booking',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hostel.booking',
            'res.id': new_booking.id,
            'target': 'new'
        }
