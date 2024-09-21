{
    "name": "Hospital Management System",
    "summary": "A system that manages hospital",
    "description": """
        This is an app that allows end-users to manage their hospital system.
    """,
    "author": "Safa Suliman",
    "category": "",
    "version": "17.0.0.1.0",
    "depends": ['base', 'crm'],
    "application": True,
    "data": [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/doctor_view.xml',
        'views/dept_view.xml',
        'views/patient_view.xml',
        'views/customer_view.xml',
        'report/patient_print.xml',
        'wizard/new_log_history_wizard_view.xml',
    ],
}
