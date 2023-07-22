from odoo import models, fields, api, _ 

class TaskWizard(models.TransientModel) :
    _name = 'task.wizard'
    _description = "Task Filter Wizard"

    is_all_project = fields.Boolean(string="All Project")
    project_name_id = fields.Many2one('project.projects',string="Project Name")
    employee_ids = fields.Many2many('hr.employee', string="Employees", default=lambda self: self._get_current_employee_ids())
    
    # def _get_current_employee_ids(self):
    #     user = self.env.user
    #     if not user.has_group('jidoka_ktsi_leave.group_leave_manager'):
    #         employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
    #         return [(4, employee.id)] if employee else []
    #     else :
    #         return []

    def _get_current_employee_ids(self):
        user = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
        return [(4, employee.id)] if employee else []


    def show_task_line(self):
        user_id = self.env.user
        if self.is_all_project :
            domain = []
        else :
            domain = [
                ('project_id', '=', self.project_name_id.id),
            ]
        
        task_line = self.env['sprint.backlog'].search(domain)
        
        action = self.env.ref('project_alda.sprint_backlog_action')
        result = action.read()[0]
        result['domain'] = domain
        result['context'] = {
            'create' : False,
            'edit' : True,
            'delete' : False,
            'default_project_name_id': self.project_name_id.id,
            'default_employee_ids': self.employee_ids.ids,
            
        }
        
        return result