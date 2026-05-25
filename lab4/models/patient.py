from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    email = fields.Char(string='Email')
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()

    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ])

    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()

    # Auto-calculated from birth_date
    age = fields.Integer(compute='_compute_age', store=True)

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    department_id = fields.Many2one(
        'hms.department',
        domain=[('is_opened', '=', True)],
    )
    department_capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many('hms.doctor')
    log_ids = fields.One2many('hms.patient.log', 'patient_id')

    # ------------------------------------------------------------------ #
    #  Computed
    # ------------------------------------------------------------------ #

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                b = rec.birth_date
                rec.age = (
                    today.year - b.year
                    - ((today.month, today.day) < (b.month, b.day))
                )
            else:
                rec.age = 0

    # ------------------------------------------------------------------ #
    #  Constraints
    # ------------------------------------------------------------------ #

    @api.constrains('email')
    def _check_email(self):
        pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        for rec in self:
            if rec.email:
                if not re.match(pattern, rec.email):
                    raise ValidationError(
                        'Please enter a valid email address.'
                    )
                duplicate = self.search([
                    ('email', '=', rec.email),
                    ('id', '!=', rec.id),
                ])
                if duplicate:
                    raise ValidationError(
                        f'Email "{rec.email}" is already used by another patient.'
                    )

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError(
                    'CR Ratio is required when PCR is checked.'
                )

    # ------------------------------------------------------------------ #
    #  Onchange
    # ------------------------------------------------------------------ #

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR checked automatically because age is under 30.',
                }
            }

    # ------------------------------------------------------------------ #
    #  State action methods (called by header buttons)
    # ------------------------------------------------------------------ #

    def action_set_undetermined(self):
        self.write({'state': 'undetermined'})

    def action_set_good(self):
        self.write({'state': 'good'})

    def action_set_fair(self):
        self.write({'state': 'fair'})

    def action_set_serious(self):
        self.write({'state': 'serious'})

    # ------------------------------------------------------------------ #
    #  Override write – log state changes
    # ------------------------------------------------------------------ #

    def write(self, vals):
        result = super().write(vals)
        if 'state' in vals:
            for rec in self:
                self.env['hms.patient.log'].create({
                    'patient_id': rec.id,
                    'description': f"State changed to {vals['state']}",
                })
        return result
