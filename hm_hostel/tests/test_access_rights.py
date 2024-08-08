from odoo.addons.hm_hostel.tests.common  import TestCommon
from odoo.tests import tagged
from odoo.exceptions import AccessError
@tagged('post_install', '-at_install', 'access', 'hostel')
class AccessRights(TestCommon):
    def test_access_hostel_room(self):
        """Hostel user have no access to create hostel room"""
        with self.assertRaises(AccessError):
            self.env['hostel.room'].with_user(self.hostel_user).create(
            {
                'name': 'Room 501 Test',
                'type': 'shared',
                'price': '150',
                'currency_id': self.currency
            })

    def test_access_hostel_bed(self):
        """Hostel user have no access to create hostel bed"""
        with self.assertRaises(AccessError):
            self.env['hostel.bed'].with_user(self.hostel_user).create(
            {
                'name': 'Room 501 - Bed 1 Test',
                'room_id': self.room_test
            })

    def test_access_hostel_service_type(self):
        """Hostel user have no access to create hostel service type"""
        with self.assertRaises(AccessError):
            self.env['hostel.service.type'].with_user(self.hostel_user).create(
            {
                'name': 'Parking Test',
                'is_available': True,
                'price': 16,
                'currency_id': self.currency
            })