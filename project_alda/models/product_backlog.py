from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ProductBacklog(models.Model):
    _name = 'product.backlog'
    _inherit = 'mail.thread'
    _description = 'Product Backlog'
    
    name = fields.Char(string="Product Backlog No.", tracking=True, default=lambda self: _('New'), readonly=True)
    pb_name = fields.Char(string="Product Backlog Name")
    project_no = fields.Many2one('project.projects', string="Project No.")
    project_name = fields.Char("Project Name", tracking=True, required=True, related="project_no.project_name")
    customer_id = fields.Many2one('res.users', string="Customer", tracking=True, required=True, related="project_no.customer_id")
    description = fields.Text(string="Description")
    priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')] ,string="Priority", tracking=True)
    wd_plan = fields.Integer(string="Work Duration Plan")
    wd_time = fields.Selection([('year', 'Year'), ('month', 'Month'), ('day', 'Day')], default='day', string=" ", required=True)
    progress = fields.Integer(string="Progress", tracking=True)
    persen = fields.Char(string="Persen", default="%", readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string="State", default='draft')
    is_auto = fields.Boolean(string="Is Auto", default=False)
    sb_count = fields.Integer(string="Sprint Backlog Count", compute="_compute_sb_count")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('product.backlog') or '/'
        return super(ProductBacklog, self).create(vals_list)
    
    def action_confirm(self):
        if self.description and self.priority and self.wd_plan and self.wd_time and self.progress :
            self.state='confirm'
        else :
            raise ValidationError("Please complete all fields")

    def insert_sb(self):
        return {
            'name': 'Sprint Backlog',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sprint.backlog',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {
                'default_project_id': self.project_no.id,
                'default_project_name': self.project_name,
                'default_pb_id': self.id,
                'default_pb_name': self.pb_name,
                'default_customer_id': self.customer_id.id,
            },
        }
    
    def _compute_sb_count(self):
        for record in self:
            record.sb_count = self.env['sprint.backlog'].search_count(
                [('pb_id', '=', self.id)])

    def view_sb(self):
        return {
            'name': 'Sprint Backlog',
            'view_type': 'tree',
            'view_mode': 'tree,form',
            'res_model': 'sprint.backlog',
            'type': 'ir.actions.act_window',
            'domain':[('pb_id', '=', self.id)],
            'context': "{'create': False,'edit':True,'delete':True}"
        }