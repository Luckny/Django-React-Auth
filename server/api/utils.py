import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import exception_handler
from rest_framework.response import Response


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


def custom_exception_handler(exc, context):
    if isinstance(exc, AuthenticationFailed):
        print(exc)
        return Response({"token": str(exc)}, status=401)
    elif str(exc) == "No OneTimePassword matches the given query.":
        return Response({"wrongOTP": str(exc)}, status=404)
    elif str(exc) == "one time password expired":
        return Response({"expiredOTP": str(exc)}, status=403)

    # else
    # default case
    return Response({"error": str(exc)}, status=500)
