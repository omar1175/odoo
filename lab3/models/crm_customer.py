from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    """
    Extend the CRM Customer (res.partner) model with HMS integration.
    """
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        'hms.patient',
        string='Related Patient',
    )

    # Make Tax ID (vat) mandatory for customers
    vat = fields.Char(required=True)

    # ------------------------------------------------------------------ #
    #  Constraints
    # ------------------------------------------------------------------ #

    @api.constrains('email', 'related_patient_id')
    def _check_email_not_in_patients(self):
        """
        A customer's email must not already exist in the patient model.
        """
        for rec in self:
            if rec.email:
                patient = self.env['hms.patient'].search([
                    ('email', '=', rec.email),
                ], limit=1)
                if patient:
                    raise ValidationError(
                        f'The email "{rec.email}" already belongs to patient '
                        f'"{patient.first_name} {patient.last_name}". '
                        'Please use a different email for this customer.'
                    )

    # ------------------------------------------------------------------ #
    #  Prevent deletion when linked to a patient
    # ------------------------------------------------------------------ #

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise UserError(
                    f'Cannot delete customer "{rec.name}" because they are '
                    f'linked to patient '
                    f'"{rec.related_patient_id.first_name} '
                    f'{rec.related_patient_id.last_name}". '
                    'Please remove the patient link first.'
                )
        return super().unlink()
