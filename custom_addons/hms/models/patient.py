from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import re

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'f_name'

    f_name = fields.Char("First Name", required=True)
    l_name = fields.Char("Last Name", required=True)
    user_id = fields.Many2one('res.users')
    b_date = fields.Date("Birth Date")
    image = fields.Char("Image")
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('o+', 'o+'),
        ('o-', 'O-'),
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
    ])
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ] , default='undetermined')
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True, readonly=True)
    email = fields.Char(required=True)

    dept_id = fields.Many2one('hms.dept', string='Department', domain=[
        ('is_open', '=', True)
    ], required=True)
    doctor_ids = fields.Many2many('hms.doctor', readonly=True)
    log_history_ids = fields.One2many('hms.patient.log', 'patient_id')
    hide_log_history = fields.Boolean(compute='_compute_hide_log_history', store='True')

    @api.depends('b_date')
    def _compute_age(self):
        for rec in self:
            if rec.b_date:
                today = fields.Date.today()
                rec.age = relativedelta(today, rec.b_date).years
            else:
                rec.age = 0

    @api.onchange('age')
    def _onchange_age(self):
        for rec in self:
            if rec.age < 30:
                rec.pcr = True
            else:
                rec.pcr = False

    @api.depends('pcr')
    def _compute_cr_ratio(self):
        for rec in self:
            if rec.pcr:
                rec.cr_ration = True
            else:
                rec.cr_ration = False

    @api.depends('age')
    def _compute_hide_log_history(self):
        for rec in self:
            rec.hide_log_history = rec.age < 50

    @api.onchange('dept_id')
    def _onchange_dept_id(self):
        for rec in self:
            if rec.dept_id:
                doctor_ids = self.env['hms.doctor'].search([('dept_id', '=', rec.dept_id.id)]).ids
                rec.doctor_ids = doctor_ids
            else:
                rec.doctor_ids = [()]

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr:
                if rec.cr_ratio <= 0:
                    raise ValidationError("CR Ratio cannot be 0 .")
                if rec.cr_ratio == 0:
                    raise ValidationError("CR Ratio cannot be 0.")

    @api.constrains('email')
    def check_email(self):
        for rec in self:
            if rec.email:
                if self.search([('email', '=', rec.email),
                                ('id', '!=', rec.id)
                                ]):
                    raise ValidationError("Email address should be unique.")
                regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(regex, rec.email):
                    raise ValidationError("Invalid email address.")

    def _log_state_change(self,old_state, new_state):
        log_data = {
            "patient_id": self.id,
            "description": f"State has been changed from {old_state} to {new_state}",
            "old_state": old_state,
            "new_state": new_state
        }
        self.env['hms.patient.log'].create(log_data)

    def action_set_state(self, new_state):
        if new_state not in ["good", "fair", "serious"]:
            raise ValidationError("Invalid state.")
        old_state = self.state
        self.state = new_state
        self._log_state_change(old_state, new_state)


    def action_good(self):
        self.action_set_state('good')

    def action_fair(self):
        self.action_set_state('fair')

    def action_serious(self):
        self.action_set_state('serious')

    def action_new_log_history_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('hms.new_log_history_action')
        action['context'] = {
            'default_patient_id': self.id
        }
        return action


class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient')
    description = fields.Text()
    old_state = fields.Char()
    new_state = fields.Char()
