from odoo import api, fields, models, _


class JidokaEmployeeGroup(models.Model):
    _name = 'jidoka.employee.group.wiz'
    _description = 'Employee Group Wizard'

    
    employee_ids = fields.Many2many(
        string='Employees',
        comodel_name='hr.employee',
        relation='emp_group_wiz_rel',
    )
    
    group_id = fields.Many2one(comodel_name='jidoka.employee.group', string='Employee Group')
    
    
    def action_add_employees(self):
        for rec in self.employee_ids:
            rec.write({
                'emp_group_id': self.group_id.id
            })
        
class EmployeeInherit(models.Model):
    _inherit = 'jidoka.employee.group'
    
    def add_employee_to_group_wiz(self):
        return {
            'name': _('Add Employee to Group'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'jidoka.employee.group.wiz',
            'target': 'new',
            'context': {'default_group_id': self.id},
        }
        
    
    

        