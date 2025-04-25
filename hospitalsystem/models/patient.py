import logging
import requests
from odoo import api, models, fields
from datetime import date, timedelta, datetime
from odoo.exceptions import UserError
import qrcode
from io import BytesIO

_logger = logging.getLogger(__name__)
_logger.info(">>>> HospitalPatient model loaded <<<<")



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital System'

    name = fields.Char(string='Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    start_date1 = fields.Date(string="Start Date")
    end_date1 = fields.Date(string="End Date")
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email')
    appointement_count = fields.Integer(
        string='Appointement Count',
        compute="_compute_count",
        store=True
    )
    country_id = fields.Many2one('res.country', string="Country", default=lambda self: self.env.ref('base.et').id)
    state_id = fields.Many2one('res.country.state', string="State/Region", domain="[('country_id', '=', country_id)]")
    qr_code = fields.Binary("QR Code", compute='_generate_qr_code', store=True)  # Store the QR code to persist it

    @api.depends('name', 'phone')  # Dependencies are for fields that are used in QR code generation
    def _generate_qr_code(self):
        for patient in self:
            if patient.name:  # Ensure patient has a name
                try:
                    # Generate QR code based on the patient's name
                    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
                    qr.add_data(patient.name)  # You can customize the data to encode
                    qr.make(fit=True)

                    # Create the image of the QR code
                    img = qr.make_image(fill="black", back_color="black")

                    # Save the image into a binary field
                    img_io = BytesIO()
                    img.save(img_io, 'PNG')
                    img_io.seek(0)

                    # Assign the binary data to the field
                    patient.qr_code = img_io.read()
                except Exception as e:
                    _logger.error(f"Error generating QR code for patient {patient.name}: {e}")
                    patient.qr_code = False  # Set to False if QR code generation fails

            else:
                # If there's no name, clear the QR code field (optional)
                patient.qr_code = False

    
    def viewdata(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'View Appointements',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointement',
            'domain': [('patient_id', '=', self.id)],
            'target': 'new',
        }

    def createData(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'View Appointements',
            'view_mode': 'form',
            'res_model': 'hospital.appointement',
            'target': 'new',
        }

    @api.depends()
    def _compute_count(self):
        for record in self:  # Added loop
            record.appointement_count = self.env['hospital.appointement'].search_count([])  # corrected search


    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year - (
                        (today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            else:
                rec.age = 0

    def send_patient_email(self):
        template_id = self.env.ref('hospitalsystem.email_template_hospital_patient').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        #
        # for patient in self:
        #     if template_id and patient.email:
        #         template_id.send_mail(patient.id, force_send=True)
