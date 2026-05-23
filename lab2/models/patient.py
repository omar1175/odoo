from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)

    birth_date = fields.Date()

    history = fields.Html()

    cr_ratio = fields.Float()

    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ])

    pcr = fields.Boolean()

    image = fields.Binary()

    address = fields.Text()

    age = fields.Integer()

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined')

    department_id = fields.Many2one(
        'hms.department',
        domain=[('is_opened', '=', True)]
    )

    department_capacity = fields.Integer(
        related='department_id.capacity'
    )

    doctor_ids = fields.Many2many(
        'hms.doctor'
    )

    log_ids = fields.One2many(
        'hms.patient.log',
        'patient_id'
    )

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True

            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR checked automatically'
                }
            }

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError(
                    'CR Ratio is required when PCR is checked'
                )

    def write(self, vals):

        old_state = self.state

        result = super().write(vals)

        if 'state' in vals:
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'description':
                    f"State changed to {vals['state']}"
            })

        return result