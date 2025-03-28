from jinja2 import Template

from app.integrations.mailgun import mailgun_email
from app.utils.constants import FRONTEND_URL


def send_password_reset_email(to_email, reset_token):
    reset_url = f"{FRONTEND_URL}/reset-password-confirm?token={reset_token}"
    subject = "Reset your DoMore password"
    with open("app/templates/reset_password.html", "r") as reset_password_html:
        reset_password_template = Template(reset_password_html.read())
        rendered_template = reset_password_template.render(
            reset_url=reset_url
        )

        text = (
            "Click the link below to reset your password:\n\n"
            f"{reset_url}\n\n"
            "If you didn't request this, please ignore this email."
        )
        mailgun_email(
            to_address=to_email,
            subject=subject,
            template=rendered_template,
            text=text
        )
        return {
            "message": "Password reset email sent successfully"
        }
