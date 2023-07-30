{
    'name': "Unindra Project Management CIC",

    'summary': """
        Unindra Project Management CIC - Managing the entire project management using SCRUM""",

    'description': """
        Unindra Project Management CIC - Managing the entire project management using SCRUM
    """,

    'author': "Robi'ah Al Adawiyah",
    'website': "https://www.linkedin.com/in/robiah-al-adawiyah-odoo-consultant/",

    'category': 'Project',
    'version': '0.1',

    'depends': [
        'base',
        'project',
        'hr',
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/sequence.xml',
        'views/projects.xml',
        'views/product_backlog.xml',
        'views/sprint_planning.xml',
        'views/sprint_evaluating.xml',
        'views/sprint_backlog.xml',
        'wizard/task_filter.xml',
        'wizard/pb_wizard.xml',
        'report/report_main.xml',
        'report/report_project.xml',
        'report/report_pb.xml',
        'report/report_sp.xml',
        'report/report_sb.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}