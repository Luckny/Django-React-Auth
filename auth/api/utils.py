import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_confirmation_email(email_address, token_id, user_id):
    # Prepare data for the email template
    data = {
        "base_url": os.getenv(
            "EMAIL_CONFIRM_POST_URL"
        ),  # Base URL for confirmation link
        "token_id": str(token_id),  # Convert token ID to string
        "user_id": str(user_id),  # Convert user ID to string
    }

    # Render HTML email template
    html_message = render_to_string("api/confirm_email.html", data)

    # Create email message
    mail = EmailMessage(
        "Confirm Your Email Address",  # Subject of the email
        html_message,  # HTML content of the email
        os.environ.get("EMAIL_HOST_USER"),  # Sender's email address
        [email_address],  # Recipient's email address
    )

    # Set content subtype to HTML
    mail.content_subtype = "html"

    # Send the email
    mail.send(fail_silently=False)
