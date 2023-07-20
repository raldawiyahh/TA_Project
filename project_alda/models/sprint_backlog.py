from odoo import api, fields, models, _

class SprintBacklog(models.Model):
    _inherit = 'project.task'
    _description = 'Sprint Backlog'

    # customer_id = fields.Many2one()
    project_id = fields.Char(string="Project No.", readonly=True, default="/")
    project_name = fields.Char(string="Project Name", readonly=True)
    pb_no = fields.Char(string="Product Backlog No.", readonly=True, default="/")
    pb_name = fields.Char(string="Product Backlog Name", readonly=True)
    task_no = fields.Char(string="Task No.", readonly=True, default="/")
    # task_title = fields.Char(string="Task Title", required=True)
    task_description = fields.Char(string="Task Description")
    modul = fields.Char(string="Modul")
    # sprint_id = fields.Char('sprint.planning')
    sprint_to = fields.Char(string="Sprint To-", related="sprint_id.sprint_to")
    end_sprint = fields.Date(string="Sprint Deadline", related="sprint_id.end_sprint")
    task_deadline = fields.Date(string="Task Deadline")
    level_difficulty = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string="Level Of Difficulty")
    task_priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], string="Task Priority")



    @api.model
    def create(self, vals):
        vals['task_no'] = self.env['ir.sequence'].next_by_code('project.task')
        return super(SprintBacklog, self).create(vals)