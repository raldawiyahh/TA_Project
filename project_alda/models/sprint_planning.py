from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SprintPlanning(models.Model):
    _name = 'sprint.planning'
    _inherit = 'mail.thread'
    _description = 'Sprint Planning'

    name = fields.Char(string="Sprint Planning", compute="_compute_name")
    # name = fields.Char(string="Sprint Planning No.", tracking=True, default=lambda self: _('New'), readonly=True)
    project_id = fields.Many2one('project.projects', string="Project No.", tracking=True, required=True)
    project_name = fields.Char(string="Project Name", related='project_id.project_name', required=True, tracking=True)
    customer_id = fields.Many2one('res.users', string="Customer", related='project_id.customer_id', required=True, tracking=True)
    sprint_to = fields.Char(string="Sprint To-", required=True, tracking=True)
    sprint_title = fields.Char(string="Sprint Title", required=True, tracking=True)
    start_sprint = fields.Date(string="Start Sprint", required=True, tracking=True)
    end_sprint = fields.Date(string='End Sprint', required=True, tracking=True)
    sprint_goals = fields.Text(string='Sprint Goals', required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('end', 'End Sprint'), ('se', 'Evaluated')], string="State", readonly=True, tracking=True, default='draft')
    is_se = fields.Boolean(string="Is Sprint Evaluating", default=False)
    se_count = fields.Integer(string="SE Count", compute="_compute_se_count")
    reality_finished = fields.Date(string="Reality Finished")
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    date_today = fields.Date(string="Date Today", default=fields.Date.today())
    pm_id = fields.Many2one('res.users', string="Project Manager", related="project_id.pm_id")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         vals['name'] = self.env['ir.sequence'].next_by_code('sprint.planning') or '/'
      
    @api.depends('project_name')
    def _compute_name(self):
        for record in self:
            record.name = record.project_name + (" - " + record.sprint_to if record.sprint_to else "")

    def action_confirm(self):
        duplicates = self.search([('id', '!=', self.id), ('project_name', '=', self.project_name), ('sprint_to', '=', self.sprint_to)])
        if duplicates:
            raise ValidationError("This project on the same 'Sprint To' is already exist!")
        elif self.start_sprint > self.end_sprint:
            raise UserError(_("Start Sprint cannot be bigger than End Sprint")) 
        else :
            self.state='confirm'

    def action_end(self):
        self.state='end'
        self.reality_finished = fields.Date.today()

    def button_se(self):
        self.is_se = True
        self.state = 'se'
        return {
            'name': 'Sprint Evaluating',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sprint.evaluating',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {
                'default_sp_id' : self.id,
                'default_project_id': self.project_id.id,
                'default_project_name': self.project_name,
                'default_customer_id': self.customer_id.id,
                'default_sprint_to' : self.sprint_to,
                'default_sprint_title' : self.sprint_title,
                'default_start_sprint' : self.start_sprint,
                'default_end_sprint' : self.end_sprint,
                'default_sprint_goals' : self.sprint_goals
            },
        }

    def _compute_se_count(self):
        for record in self:
            record.se_count = self.env['sprint.evaluating'].search_count(
                [('sp_id', '=', self.id)])

    def view_se(self):
        return {
            'name': 'Sprint Evaluating',
            'view_type': 'tree',
            'view_mode': 'tree,form',
            'res_model': 'sprint.evaluating',
            'type': 'ir.actions.act_window',
            'domain':[('sp_id', '=', self.id)],
            'context': "{'create': False,'edit':True,'delete':True}"
        }