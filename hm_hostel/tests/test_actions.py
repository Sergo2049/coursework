from datetime import date, timedelta
from odoo.addons.hm_hostel.tests.common import TestCommon
from odoo.tests import tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install', 'actions', 'hostel')
class TestActions(TestCommon):

    def test_compute_booking_days(self):
        """Tests computing booking days"""
        booking = self.env['hostel.booking'].create({
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=3),
            'visitor_id': self.visitor_test.id,
            'bed_id': self.bed_test.id,
        })
        self.assertEqual(booking.booking_days, 3, 'Booking days should be 3')

    def test_booking_is_paid(self):
        """Test booking is paid"""
        booking = self.env['hostel.booking'].create({
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=3),
            'visitor_id': self.visitor_test.id,
            'bed_id': self.bed_test.id,
        })
        self.env['hostel.payment'].create({
            'booking_id': booking.id,
            'type': 'cash',
            'amount': 300,
            'currency_id': self.env.company.currency_id.id
        })
        self.assertTrue(booking.is_paid, 'Booking should be marked as paid.')

    def test_check_dates(self):
        """Booking end date must be a least one day furthen then start date"""
        with self.assertRaises(ValidationError):
            self.env['hostel.booking'].create({
                'start_date': date.today(),
                'end_date': date.today(),
                'visitor_id': self.visitor_test.id,
                'bed_id': self.bed_test.id,
            })

    def test_phone_number_unique(self):
        """Visitirs phone number must be unique"""
        with self.assertRaises(ValidationError):
            self.env['res.partner'].create({
                'name': 'Ivan',
                'phone': '+3809998887766',
                'gender': 'male'})

            self.env['res.partner'].create({
                'name': 'Inna',
                'phone': '+3809998887766',
                'gender': 'female'})
