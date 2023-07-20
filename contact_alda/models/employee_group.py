from odoo import api, fields, models, _


class JidokaEmployeeGroup(models.Model):
    _name = 'jidoka.employee.group'
    _description = 'Employee Group'
    
    name = fields.Char(string='Name', required=True)
    
    leader_id = fields.Many2one(comodel_name='hr.employee', string='Leader', required=True)
    
    spv_id = fields.Many2one(comodel_name='hr.employee', string='Supervisor', required=True)
    
    employee_ids = fields.One2many(comodel_name='hr.employee', inverse_name='emp_group_id', string='Employee Group')
    
class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    
    emp_group_id = fields.Many2one(comodel_name='jidoka.employee.group', string='Employee Group', groups="hr.group_hr_user")
    
    

        