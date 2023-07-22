{
    'name': 'Unindra Project',
    'version': '1.0.1',
    'author': "Robi'ah Al Adawiyah",
    
    'depends': [
        'project',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sequence.xml',
        'views/projects.xml',
        'views/product_backlog.xml',
        'views/sprint_planning.xml',
        'views/sprint_evaluating.xml',
        'views/sprint_backlog.xml',
        'wizard/task_filter.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}