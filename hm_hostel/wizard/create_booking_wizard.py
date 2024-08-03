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
                             string='Bed', domain="[('id', 'in', available_bed_ids)]")

    room_id = fields.Many2one(related='bed_id.room_id', readonly=True,
                              string='Room')

    available_bed_ids = fields.Binary(compute='_compute_available_beds')

    @api.depends('planned_start_date', 'planned_end_date')
    def _compute_available_beds(self):
       for wizard in self:
           if wizard.planned_start_date and wizard.planned_end_date:
               booked_beds = self.env['hostel.booking'].search(
                   ['!','&', ('start_date', '>=', self.planned_start_date),
                    ('start_date', '<=', self.planned_end_date), '&',
                    ('end_date', '>=', self.planned_start_date),
                    ('end_date', '<=', self.planned_end_date)])
               booked_beds = booked_beds.mapped('bed_id.id')
               all_beds = self.env['hostel.bed'].search([]).ids
               available_beds = list(set(all_beds) - set(booked_beds))

               print(f'Booked beds:{booked_beds}')
               print(f'Booked beds:{available_beds}')

               wizard.available_bed_ids = available_beds
           else:
               wizard.available_bed_ids = []

    def action_create_booking(self):
        booking_vals = {
            'start_date': self.planned_start_date,
            'end_date': self.planned_end_date,
            'visitor_id': self.visitor_id.id,
            'bed_id': self.bed_id.id,
            'state': 'planned'
        }
        # new_booking = self.env['hostel.booking'].create(booking_vals)
        # return {'type': 'ir.actions.act_window_close'}

        return {
            'name': 'New booking',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hostel.booking',
            # 'res_id': new_booking.id,
            'target': 'new',
            'context': {
                'default_start_date': self.planned_start_date,
                'default_end_date': self.planned_end_date,
                'default_visitor_id': self.visitor_id.id,
                'default_bed_id': self.bed_id.id,
            }
        }
