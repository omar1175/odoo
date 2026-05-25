{
    'name': 'HMS',
    'version': '1.1',
    'summary': 'Hospital Management System',
    'category': 'Hospital',
    'depends': ['base', 'contacts', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/crm_customer_views.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Omar Abdelstar',
    'license': 'LGPL-3',
}
