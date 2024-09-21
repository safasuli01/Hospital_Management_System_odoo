from odoo import models, fields

class Ticket(models.Model):
    _name = 'td.ticket'
    _description = 'Ticket'

    name = fields.Char()
    number = fields.Integer()
    tag = fields.Char()
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done')
    ], default='new')
    file = fields.Binary()
    description = fields.Text()

    def action_new(self):
        self.state = 'new'

    def action_doing(self):
        self.state = 'doing'

    def action_done(self):
        self.state = 'done'