from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def write(self, vals):
        stage_changed = False
        old_stage_id = self.stage_id.id
        old_stage_name = self.stage_id.name if self.stage_id else None
        new_stage_id = vals.get('stage_id', False)

        res = super(CrmLead, self).write(vals)

        if new_stage_id and old_stage_name:
            new_stage = self.env['crm.stage'].browse(new_stage_id)
            new_stage_name = new_stage.name

            # Only send if stage changed from "New" to "Qualified"
            if old_stage_name == "New" and new_stage_name == "Qualified":
                # Find users in the group 'group_notify_on_qualified'
                notify_group = self.env.ref('email_notification.group_notify_on_qualified')
                users_to_notify = self.env['res.users'].search([
                    ('groups_id', 'in', notify_group.id)
                ])

                for user in users_to_notify:
                    if user.email:
                        self.send_stage_change_email(user, old_stage_name, new_stage_name)

        return res

    def send_stage_change_email(self, user, old_stage_name, new_stage_name):
        mail_values = {
            'subject': f'Lead "{self.name}" moved to {new_stage_name}',
            'body_html': f"""
                <p>Hello {user.name},</p>
                <p>The lead <strong>{self.name}</strong> has moved from
                <strong>{old_stage_name}</strong> to <strong>{new_stage_name}</strong>.</p>
                <p>Regards,<br/>Your CRM System</p>
            """,
            'email_to': user.email,
            'author_id': self.env.user.partner_id.id,
            'model': 'crm.lead',
            'res_id': self.id,
        }

        self.env['mail.mail'].create(mail_values).send()
