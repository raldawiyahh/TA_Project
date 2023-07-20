from odoo import api, fields, models, _


class MrpProductionEmployeeGroup(models.Model):
    _inherit = 'mrp.production'

    @api.onchange('operator_id')
    def _onchange_operator_id(self):
        if self.operator_id and self.operator_id.emp_group_id:
            leader = self.operator_id.emp_group_id.leader_id
            self.leader_id = leader.id
    
    