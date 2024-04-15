import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_confirmation_email(email_address, code, user_id):

    # Render HTML email template
    html_message = render_to_string("api/confirm_email.html", {"code": code})

    # Create email message
    mail = EmailMessage(
        "Here's your verification code",  # Subject of the email
        html_message,  # HTML content of the email
        os.environ.get("EMAIL_HOST_USER"),  # Sender's email address
        [email_address],  # Recipient's email address
    )

    # Set content subtype to HTML
    mail.content_subtype = "html"

    # Send the email
    mail.send(fail_silently=False)
