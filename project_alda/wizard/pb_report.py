from odoo import models, fields, api, _ 

class ProductBacklogReportWizard(models.TransientModel) :
    _name = 'pb.report.wizard'
    _description = "Product Backlog Report Wizard"

    name = fields.Char(string="Name")
    project_no = fields.Many2one('project.projects', string="Project No.")
    project_name = fields.Char(string="Project Name", related="project_no.project_name")

    def action_print_excel(self):
        self.name = "Product Backlog Report"
        data = {
            'form_data': self.read()[0]
        }
        report = self.env.ref('project_alda.pb_xlsx')
        if self.name:
            report.sudo().write({'name': self.name})
        else:
            report.sudo().write({'name': "Product Backlog Report"})
        return report.report_action(self, data=data)
    
    
class ProductBacklogReportXLSX(models.AbstractModel):
    _name = 'report.project_alda.pb_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, tr):
        project = tr.project_no
        self.pb_report(workbook, data, tr, project)
        workbook.close()

        
    def pb_report(self, workbook, data, tr, project):
        project_no = project | project.mapped('child_ids')
        products = self.env['product.backlog'].sudo().search(project_no, order='name asc')

        
        # style
        title_center_header1 = workbook.add_format()
        title_center_header1.set_align('center')
        title_center_header1.set_align('vcenter')
        title_center_header1.set_font_size(20)
        title_center_header1.set_font_name('Times New Roman')
        title_center_header1.set_bold()

        title_center_header2 = workbook.add_format()
        title_center_header2.set_align('center')
        title_center_header2.set_align('vcenter')
        title_center_header2.set_font_size(14)
        title_center_header2.set_font_name('Times New Roman')

        title_center = workbook.add_format()
        title_center.set_align('center')
        title_center.set_align('vcenter')
        title_center.set_font_size(11)
        title_center.set_font_name('Times New Roman')
        
        date_format = workbook.add_format()
        date_format.set_align('center')
        date_format.set_align('vcenter')
        date_format.set_font_size(12)
        date_format.set_font_name('Times New Roman')
        # date_format.set_bg_color('#242424')
        date_format.set_font_color('white')
        date_format.set_bold()
        
        text_format_left = workbook.add_format()
        text_format_left.set_align('left')
        text_format_left.set_align('vcenter')
        text_format_left.set_border()
        text_format_left.set_font_size(12)
        text_format_left.set_font_name('Times New Roman')
        
        row = 0
        col = 0
        sheet.set_row(1, 100, 20)

        for product in products :
            sheet.merge_range(row,3, row, 9, "PT CIC CONSULTING", title_center_header1)
            row += 1
            sheet.merge_range(row,3, row, 9, "Leading in Digital Transformation", title_center_header2)
            row += 1
            sheet.merge_range(row,3, row, 9, "Jl. Kb. Pedes No. 15, Kec. Tanah Sereal, Bogor, Jawa Barat, Indonesia, Kode Pos 12620", title_center)
            row += 1
            sheet.merge_range(row,3, row, 9, "Email : contact@cic-integration.co Website : https://cic-integration.co/ Telp : 0251-833-7342", title_center)
            row += 1

