from datetime import timedelta
from odoo import api, fields, models


class CreateBookingWizard(models.TransientModel):
    _name = 'create.booking.wizard'
    _description = 'Create Booking Wizard'

    planned_start_date = fields.Date(required=True,
                                     default=fields.Date.today())

    planned_end_date = fields.Date(required=True,
                                   default=fields.Date.today()
                                   + timedelta(days=1))

    visitor_id = fields.Many2one('res.partner', required=True,
                                 string='Visitor')

    bed_id = fields.Many2one('hostel.bed', required=True,
                             string='Bed',
                             domain="[('id', 'in', available_bed_ids)]")

    room_id = fields.Many2one(related='bed_id.room_id', readonly=True,
                              string='Room')

    available_bed_ids = fields.Binary(compute='_compute_available_beds')

    @api.depends('planned_start_date', 'planned_end_date')
    def _compute_available_beds(self):
        self.ensure_one()
        if self.planned_start_date and self.planned_end_date:

            domain = [('state', '!=', 'canceled'),
                      ('start_date', '<=', self.planned_end_date),
                      ('end_date', '>=', self.planned_start_date)]
            if self.id:
                domain.append(('id', '!=', self.id))
            booked_beds = self.env['hostel.booking'].search(domain)

            booked_beds = booked_beds.mapped('bed_id.id')
            all_beds = self.env['hostel.bed'].search([]).ids
            available_beds = list(set(all_beds) - set(booked_beds))
            self.available_bed_ids = available_beds
        else:
            self.available_bed_ids = []

    def action_create_booking(self):
        self.ensure_one()
        return {
            'name': 'New booking',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hostel.booking',
            'target': 'new',
            'context': {
                'default_start_date': self.planned_start_date,
                'default_end_date': self.planned_end_date,
                'default_visitor_id': self.visitor_id.id,
                'default_bed_id': self.bed_id.id,
            }
        }
