{
    'name': 'Hospital Management System',
    'version': '1.0',
    'summary': 'Manage patients in a hospital',
    'category': 'Healthcare',
    'author': 'Wafaey',
    'depends': ['base'],       
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/menus.xml',
        'views/customer_views.xml',
        'reports/patient_status_report.xml',
    ],     
}