from odoo import models,fields

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctors'
    _rec_name = 'f_name'

    f_name = fields.Char("First Name")
    l_name = fields.Char("Last Name")
    image = fields.Image()
    dept_id = fields.Many2one('hms.dept', string='Department')
