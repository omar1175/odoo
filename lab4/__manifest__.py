{
    'name': 'HMS',
    'version': '1.2',
    'summary': 'Hospital Management System',
    'category': 'Hospital',
    'depends': ['base', 'contacts', 'crm'],
    'data': [
        # Security — groups must be loaded FIRST
        'security/hms_groups.xml',
        'security/ir.model.access.csv',
        'security/hms_record_rules.xml',

        # Views
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/crm_customer_views.xml',

        # Reports
        'report/patient_report_template.xml',
        'report/patient_report_action.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Omar Abdelstar',
    'license': 'LGPL-3',
}
