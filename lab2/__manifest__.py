{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'category': 'Hospital',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'Omar Abdelstar',
    'license': 'LGPL-3',
}