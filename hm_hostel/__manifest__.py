# Copyright 2024 Serhii Vydysh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Hm Hostel',
    'description': """
        Hostel management""",
    'version': '17.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Serhii Vydysh',
    'depends': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/hm_hostel_groups.xml',
        'views/hostel_menu.xml',
        'views/hostel_service_type.xml',
        'views/hostel_service.xml',
        'views/hostel_bed.xml',
        'views/hostel_visitor.xml',
        'views/hostel_room.xml',
        'views/hostel_payment.xml',
        'wizard/create_booking_wizard_view.xml',
        "wizard/create_report_booking_profit_wizard.view.xml",
        'views/hostel_booking.xml',
        'reports/report_booking.xml',
        'reports/report_booking_profit.xml',
    ],
    'demo': [
        'demo/hostel_demo.xml',
    ],
}
