from odoo import api, fields, models


class HostelBed(models.Model):

    _name = "hostel.bed"

    _description = "Hostel Bed"

    name = fields.Char(string='Bed', required=True,
                       help='Bed number', translate=True)

    room_id = fields.Many2one(comodel_name='hostel.room',
                              required=True)
    booking_ids = fields.One2many('hostel.booking',
                                  'bed_id',
                                  string='Bokings', readonly=True,
                                  domain=[('state', '!=', 'canceled')])

    @api.depends('room_id')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.room_id.name}-{rec.name}'
