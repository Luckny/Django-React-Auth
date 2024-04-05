from django.core.mail import send_mail
from django.template.loader import get_template


def send_confirmation_email(email, token_id, user_id):
    data = {"token_id": str(token_id), "user_id": str(user_id)}

    message = get_template("api/confirm_email.txt").render(data)
    send_mail(
        "Confirm email",
        message,
        "admin@admin.com",
        [email],
        fail_silently=False,
    )
