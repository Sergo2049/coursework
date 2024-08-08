from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta

class TestCommon(TransactionCase):
    def setUp(self):
        super(TestCommon, self).setUp()
        self.group_hostel_user = self.env.ref('hm_hostel.group_hostel_user')
        self.group_hostel_trainee = self.env.ref('hm_hostel.group_hostel_trainee')
        self.group_hostel_manager = self.env.ref('hm_hostel.group_hostel_manager')
        self.hostel_user = self.env['res.users'].create({
            'name': 'Hostel User Test',
            'login': 'hostel_user_test',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_hostel_user.id)]
        })
        self.hostel_trainee = self.env['res.users'].create({
            'name': 'Hostel Trainee Test',
            'login': 'hostel_trainee_test',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_hostel_trainee.id)]
        })
        self.hostel_manager = self.env['res.users'].create({
            'name': 'Hostel Manager Test',
            'login': 'hostel_manager_test',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_hostel_manager.id)]
        })
        self.currency = self.env.company.currency_id.id
        self.visitor_test = self.env['hostel.visitor'].create({
            'first_name':'Ivan',
            'last_name': 'Ivanov',
            'phone': '+380945678899',
            'gender': 'male'
        })
        self.room_test = self.env['hostel.room'].create({
            'name': 'Room 901 Test',
            'type': 'shared',
            'price': 100,
            'currency_id': self.env.company.currency_id.id
        })
        self.bed_test = self.env['hostel.bed'].create({
            'name': 'Bed 1',
            'room_id': self.room_test.id
        })
        self.booking_test = self.env['hostel.booking'].create({
            'start_date': fields.date.today(),
            'end_date': fields.date.today() + timedelta(days=3),
            'visitor_id': self.visitor_test.id,
            'bed_id': self.bed_test.id
        })
        self.service_type_test = self.env['hostel.service.type'].create({
            'name': 'Breakfast Test',
            'is_available': 'True',
            'price': 15,
            'currency_id': self.env.company.currency_id.id
        })
        self.service_test = self.env['hostel.service'].create({
            'service_type_id': self.service_type_test.id,
            'price': 20,
            'booking_id': self.booking_test.id
        })
        self.payment_test = self.env['hostel.payment'].create({
            'amount': 50,
            'booking_id': self.booking_test.id,
        })

