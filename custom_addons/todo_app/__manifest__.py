{
    "name": "ToDo App",
    "summary": "To Do Tasks Management",
    "description": """
            This is an app that allows end-users to manage their to-do tasks.
    """,
    "author": "Safa Suliman",
    "category": "",
    "version": "17.0.0.1.0",
    "depends":['base'],
    "application": True,
    "data" : [
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/ticket_view.xml',
    ]
}