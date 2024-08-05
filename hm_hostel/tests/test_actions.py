from odoo.addons.hm_hostel.tests.common  import TestCommon
from odoo.tests import tagged
from odoo.exceptions import AccessError
from datetime import date, timedelta

@tagged('post_install' 'hostel' 'action')
class TestActions(TestCommon):
    def test_compute_booking_days(self):
        booking = self.env['hostel.booking'].create({
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=3),
            'visitor_id': self.visitor_test.id,
            'bed_id': self.bed_test.id,
        })
        self.assertEqual(booking.booking_days, 3, 'Booking days should be 3')