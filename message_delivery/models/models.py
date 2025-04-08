from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)


class HospitalPatient(models.Model):
    _name = 'message.delivery'
    _description = 'Hospital Patient'

    # Fields for the patient information
    name = fields.Char(string='Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for patient in self:
            if patient.date_of_birth:
                today = fields.Date.context_today(self)
                birth_date = fields.Date.from_string(patient.date_of_birth)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                patient.age = age

    def send_sms(self):
        # This method assumes it's being called from an instance of the hospital.patient model
        for patient in self:
            recipient_phone = patient.phone
            patient_name = patient.name

            if not recipient_phone:
                _logger.error(f"No phone number provided for patient: {patient_name}")
                return

            # Afro Message API settings
            base_url = 'https://api.afromessage.com/api/send'
            token = 'eyJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiOUZ3aDdMQzhnSjdnd2VIb001RHhQRVY0YW5QV0JzQkkiLCJleHAiOjE5MDEwMDU5NzQsImlhdCI6MTc0MzIzOTU3NCwianRpIjoiMGY4ZjdlMTQtMDU0Yy00Yjk1LThjN2UtZjk3NjMxNDdlMjcyIn0.OmIUt0QG2DHRc4fDg0RsW6twBRob-O3f2AshYyd3MxA'  # Replace with your real API token
            sender_name = 'e80ad9d8-adf3-463f-80f4-7c4b39f7f164'  # Replace with your sender name/ID
            callback_url = 'google.com'  # Optional: Replace with your callback URL if any

            # SMS message
            message = f'Hello {patient_name}, welcome to our hospital!'

            # Prepare the request headers and parameters
            headers = {
                'Authorization': f'Bearer {token}',
            }

            # Request parameters
            params = {
                'sender': sender_name,
                'to': '0908096189',
                'message': message,
                'callback': callback_url
            }

            # Send the SMS request
            try:
                response = requests.get(base_url, headers=headers, params=params)
                response.raise_for_status()  # Automatically raises HTTPError for bad responses
                json_response = response.json()
                if json_response.get('acknowledge') == 'success':
                    _logger.info(f'SMS sent successfully to {recipient_phone}')
                else:
                    _logger.error(f'Failed to send SMS: {json_response.get("response", {}).get("errors")}')
            except requests.exceptions.RequestException as e:
                _logger.error(f'Error while sending SMS to {recipient_phone}: {e}')
            except Exception as e:
                _logger.error(f'Unexpected error while sending SMS to {recipient_phone}:{e}')

