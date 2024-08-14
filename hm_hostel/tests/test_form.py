from odoo.addons.hm_hostel.tests.common import TestCommon
from odoo.tests import tagged
from odoo.tests.common import Form


@tagged('post_install', '-at_install', 'form', 'hostel')
class TestForm(TestCommon):
    def test_new_booking_status(self):
        """Default booking status must be planned"""
        booking_form = Form(self.booking_test)
        booking_form.save()
        self.assertEqual(booking_form.state, 'planned')

    def test_new_payment_type(self):
        """Default payment type must be credit card"""
        payment_form = Form(self.payment_test)
        self.assertEqual(payment_form.type, 'credit_card')
