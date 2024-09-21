from odoo import models,fields

class Dept(models.Model):
    _name = 'hms.dept'
    _description = 'Departments'

    name = fields.Char()
    capacity = fields.Integer()
    is_open = fields.Boolean()
    patient_ids = fields.One2many('hms.patient','dept_id')
