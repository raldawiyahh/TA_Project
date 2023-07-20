from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SprintEvaluating(models.Model):
    _name = 'sprint.evaluating'
    _inherit = 'mail.thread'
    _description = 'Sprint Evaluating'

    name = fields.Char(string="Sprint Evaluating", compute="_compute_name")
    sp_id = fields.Many2one('sprint.planning', string="Sprint Planning ID")
    project_id = fields.Many2one('project.projects', string="Project No.", tracking=True, required=True, related="sp_id.project_id", readonly=True)
    project_name = fields.Char(string="Project Name", related='sp_id.project_name', required=True, tracking=True, readonly=True)
    customer_id = fields.Many2one('res.users', string="Customer", related='sp_id.customer_id', required=True, tracking=True, readonly=True)
    sprint_to = fields.Char(string="Sprint To-", required=True, tracking=True, related="sp_id.sprint_to", readonly=True)
    sprint_title = fields.Char(string="Sprint Title", required=True, tracking=True, related="sp_id.sprint_title", readonly=True)
    start_sprint = fields.Date(string="Start Sprint", required=True, tracking=True, related="sp_id.start_sprint", readonly=True)
    end_sprint = fields.Date(string='End Sprint', required=True, tracking=True, related="sp_id.end_sprint", readonly=True)
    sprint_goals = fields.Text(string='Sprint Goals', required=True, related="sp_id.sprint_goals", readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", readonly=True, tracking=True, default='draft')
    evaluating_result = fields.Text(string="Evaluating Result")
    attachment = fields.Binary(string="Attachment")
    se_date = fields.Date(string="Date", required=True, readonly=True, default=fields.Date.today())
    
    @api.depends('project_name')
    def _compute_name(self):
        for record in self:
            record.name = record.project_name

    def action_confirm(self):
        duplicates = self.search([('id', '!=', self.id), ('project_name', '=', self.project_name), ('sprint_to', '=', self.sprint_to)])

        if self.evaluating_result and self.attachment:
            if not duplicates:
                self.state = 'confirm'
            else:
                raise ValidationError("This sprint planning has been evaluated")
        else:
            raise ValidationError("Please fill the 'Evaluating Result' and 'Attachment' first.")
