{
    'name': 'Jidoka Employee Group',
    'version': '1.0.1',
    'author': "Jidoka Team",
    
    'depends': [
        'hr',
        'jidoka_mpi_base',
        'jidoka_mpi_manufacturing',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/employee.xml',
        'views/employee_group.xml',
        'wizard/employee_group_wiz.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}