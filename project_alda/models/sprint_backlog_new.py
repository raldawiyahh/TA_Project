from odoo import api, fields, models, _
import pytz
from datetime import datetime

class SprintBacklog(models.Model):
    _name = 'sprint.backlog'
    _inherit = 'mail.thread'
    _description = 'Sprint Backlog'

    name = fields.Char(string="Task No.", tracking=True, default=lambda self: _('New'), readonly=True)
    task_title = fields.Char(string="Task Title", tracking=True)
    task_description = fields.Text(string="Task Description", tracking=True)
    project_id = fields.Many2one('project.projects', string="Project No.", tracking=True)
    project_name = fields.Char(string="Project Name", tracking=True, related="project_id.project_name")
    pb_id = fields.Many2one('product.backlog', string="Product Backlog No.", tracking=True, domain="[('project_no', '=', project_id)]")
    pb_name = fields.Char(string="Product Backlog Name", tracking=True, related="pb_id.pb_name")
    customer_id = fields.Many2one('res.users', string="Customer", related="project_id.customer_id")
    modul = fields.Char(string="Modul", tracking=True)
    sprint_id = fields.Many2one('sprint.planning', string="Sprint Name", tracking=True, domain="[('project_id', '=', project_id)]")
    sprint_deadline = fields.Date(string="Sprint Deadline", tracking=True, related="sprint_id.end_sprint")
    task_deadline = fields.Date(string="Task Deadline", tracking=True)
    level_difficulty = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('height', 'Height')], string="Level Of Difficulty", tracking=True)
    task_priority = fields.Float(string="Task Priority", tracking=True)
    assignees_ids = fields.Many2many('res.users', string="Assignees", tracking=True)
    calculate_date = fields.Date(string="Calculate Date")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('delivered', 'Delivered'), ('progress', 'On Progress'), ('ready_check', 'Ready To Check'), ('qc', 'QC'), ('need_fix', 'Need Fix'), ('done', 'Done'), ('cancel', 'Cancel')], string="State", tracking=True, default='draft')
    state2= fields.Selection([('1', 'Preparation'), ('2', 'On Progress'), ('3', 'check'), ('4', 'Done')], string="State2", default='1')
    is_auto = fields.Boolean(string="Is Auto")
    submission_date = fields.Date(string="Submission Date")
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    color = fields.Selection([
            ('red', 'Red'),
            ('blue', 'Blue'),
            ('green', 'Green'),
            ('yellow', 'Yellow'),
            # Add more colors as needed
        ], string='Color', default='blue')


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('sprint.backlog') or '/'
        return super(SprintBacklog, self).create(vals_list)

    def button_confirm(self):
        self.state = 'confirm'
        self.state2 = '1'

    def button_delivered(self):
        self.state = 'delivered'
        self.state2 = '1'
        
    def button_progress(self):
        self.state = 'progress'
        self.state2 = '2'
        
    def button_ready_check(self):
        self.state = 'ready_check'
        self.state2 = '3'
        
    def button_qc(self):
        self.state = 'qc'
        self.state2 = '3'
        
    def button_need_fix(self):
        self.state = 'need_fix'
        self.state2 = '1'
        
    def button_done(self):
        self.state = 'done'
        self.state2 = '4'
        asia_tz = pytz.timezone('Asia/Jakarta')
        submission_date = datetime.now(asia_tz).date()
        self.submission_date = submission_date
    
    def button_cancel(self):
        self.state = 'cancel'
        self.state2 = '1'
