{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'category': 'Hospital',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
    ],
    'installable': True,
    'application': True,
}