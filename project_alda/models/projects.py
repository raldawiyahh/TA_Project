from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ProjectMockup(models.Model):
    _name = 'project.mockup'
    _description = 'Mockup'

    name = fields.Char(string="Name")
    remark = fields.Char(string="Remark")
    mockup_doc = fields.Binary(string="Mockup Document")
    url_mockup = fields.Text(string="URL")
    project_no = fields.Many2one('project.projects', string="Project No.")
    is_url = fields.Boolean(string="Is URL", compute="_compute_mockup", store=True)
    is_doc = fields.Boolean(string="Is Doc", compute="_compute_mockup", store=True)
    attachment_acc = fields.Binary(string="Attachment Accepted")
    state = fields.Selection([('draft', 'Draft'), ('acc', 'Accepted')], string="State", default='draft')
    
    @api.depends('remark')
    def _compute_name(self):
        for record in self:
            record.name = record.remark

    @api.depends('mockup_doc', 'url_mockup')
    def _compute_mockup(self):
        self.is_doc = bool(self.mockup_doc)
        self.is_url = bool(self.url_mockup)
    
    def button_accepted(self):
        if self.attachment_acc :
            self.state = 'acc'
        else :
            raise ValidationError("Please Input Attachment Accepted")

class ProjectProjects(models.Model):
    _name = 'project.projects'
    _inherit = 'mail.thread'
    _description = 'Project'
    
    name = fields.Char(string="Project No.", tracking=True, default=lambda self: _('New'), readonly=True)
    project_name = fields.Char("Project Name", tracking=True, required=True)
    start_pro = fields.Date("Start Date", tracking=True)
    end_pro = fields.Date("End Date", tracking=True)
    project_charter = fields.Binary("Project Charter", tracking=True)
    req_gathering = fields.Binary("Req. Gathering", tracking=True)
    blueprint = fields.Binary("Blueprint", tracking=True)
    # project_mockup = fields.Binary("Project Mockup", tracking=True)
    customer_id = fields.Many2one('res.users', string="Customer", tracking=True)
    customer_pic_id = fields.Many2one('res.users', string="Customer PIC", tracking=True)
    pm_id = fields.Many2one('res.users', string="Project Manager", tracking=True)
    sa_id = fields.Many2one('res.users', string="System Analyst", tracking=True)
    tl_id = fields.Many2one('res.users', string="Team Leader", tracking=True)
    team_id = fields.Many2many('res.users', string="Team", tracking=True)
    notes = fields.Text(string="Notes", tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('accept_blu', 'Blueprint Accepted'), ('development', 'Development'), ('uat', 'UAT'), ('done', 'Done')], string="State", default='draft')
    mockup_count = fields.Integer(string="Mockup Count", compute="_compute_mockup_count")
    pb_count = fields.Integer(string="Product Backlog Count", compute="_compute_pb_count")
    sp_count = fields.Integer(string="Sprint Planning Count", compute="_compute_sp_count")  
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
            vals['name'] = self.env['ir.sequence'].next_by_code('project.projects') or '/'
        return super(ProjectProjects, self).create(vals_list)
    
    def action_confirm(self):
        if self.start_pro > self.end_pro:
            raise UserError(_("Start Project cannot be bigger than End Project"))
        else :
            self.state='confirm'

    def action_blueprint_acc(self):
        self.state='accept_blu'

    def action_development(self):
        self.state='development'
    
    def action_uat(self):
        self.state='uat'

    def action_done(self):
        self.state='done'

    def insert_mockup(self):
        return {
            'name': 'Project Mockup',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.mockup',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_project_no': self.id,
                
            },
        }
    
    def _compute_mockup_count(self):
        for record in self:
            record.mockup_count = self.env['project.mockup'].search_count(
                [('project_no', '=', self.id)])

    def view_mockup(self):
        return {
            'name': 'Project Mockup',
            'view_type': 'tree',
            'view_mode': 'tree,form',
            'res_model': 'project.mockup',
            'type': 'ir.actions.act_window',
            'domain':[('project_no', '=', self.id)],
            'context': "{'create': False,'edit':True,'delete':True}"
        }

    def insert_pb(self):
        return {
            'name': 'Product Backlog',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.backlog',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {
                'default_project_no': self.id,
                'default_project_name': self.project_name,
                'default_customer_id': self.customer_id.id,
                'default_is_auto' : True,
            },
        }
    
    def _compute_pb_count(self):
        for record in self:
            record.pb_count = self.env['product.backlog'].search_count(
                [('project_no', '=', self.id)])

    def view_pb(self):
        return {
            'name': 'Product Backlog',
            'view_type': 'tree',
            'view_mode': 'tree,form',
            'res_model': 'product.backlog',
            'type': 'ir.actions.act_window',
            'domain':[('project_no', '=', self.id)],
            'context': "{'create': False,'edit':True,'delete':True}"
        }
    
    def insert_sp(self):
        return {
            'name': 'Sprint Planning',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sprint.planning',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {
                'default_project_id': self.id,
                'default_project_name': self.project_name,
                'default_customer_id': self.customer_id.id,
            },
        }
    
    def _compute_sp_count(self):
        for record in self:
            record.sp_count = self.env['sprint.planning'].search_count(
                [('project_id', '=', self.id)])

    def view_sp(self):
        return {
            'name': 'Sprint Planning',
            'view_type': 'tree',
            'view_mode': 'tree,form',
            'res_model': 'sprint.planning',
            'type': 'ir.actions.act_window',
            'domain':[('project_id', '=', self.id)],
            'context': "{'create': False,'edit':True,'delete':True}"
        }