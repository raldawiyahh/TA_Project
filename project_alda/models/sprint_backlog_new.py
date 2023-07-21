from odoo import api, fields, models, _

class SprintBacklog(models.Model):
    _name = 'sprint.backlog'
    _inherit = 'mail.thread'
    _description = 'Sprint Backlog'

    name = fields.Char(string="Task No.", tracking=True, default=lambda self: _('New'), readonly=True)
    task_title = fields.Char(string="Task Title", tracking=True)
    task_description = fields.Text(string="Task Description", tracking=True)
    project_id = fields.Many2one('project.projects', string="Project No.", tracking=True)
    project_name = fields.Char(string="Project Name", tracking=True)
    pb_id = fields.Many2one('product.backlog', string="Product Backlog No.", tracking=True)
    pb_name = fields.Char(string="Product Backlog Name", tracking=True)
    customer_id = fields.Many2one('res.users', string="Customer")
    modul = fields.Char(string="Modul", tracking=True)
    sprint_id = fields.Many2one('sprint.planning', string="Sprint Name", tracking=True)
    sprint_deadline = fields.Date(string="Sprint Deadline", tracking=True, related="sprint_id.end_sprint")
    task_deadline = fields.Date(string="Task Deadline", tracking=True)
    level_difficulty = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('height', 'Height')], string="Level Of Difficulty", tracking=True)
    task_priority = fields.Float(string="Task Priority", tracking=True)
    assignees_ids = fields.Many2many('res.users', string="Assignees", tracking=True)
    calculate_date = fields.Date(string="Calculate Date")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('delivered', 'Delivered'), ('progress', 'On Progress'), ('ready_check', 'Ready To Check'), ('qc', 'QC'), ('need_fix', 'Need Fix'), ('done', 'Done'), ('cancel', 'Cancel')], string="State", tracking=True, default='draft')
    
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('project.task')
        return super(SprintBacklogInherit, self).create(vals)