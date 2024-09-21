from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Customer(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')
    vat = fields.Char(string="Tax ID", required=True)

    @api.constrains('email')
    def check_email_redundancy(self):
        for rec in self:
            if rec.email:
                existing_email = self.env['hms.patient'].search([]).mapped('email')
                if rec.email in existing_email:
                    raise ValidationError(f"Email {rec.email} already exists for a patient.")

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError("Cannot delete a customer record because it is related to existing patient.")

    @api.constrains('vat')
    def _check_tax_id(self):
        for rec in self:
            if not rec.vat:
                raise ValidationError("Tax ID is required.")
