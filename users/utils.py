from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .token import user_activation_token


def detect_user(user):
    """
    Redirect users based on the users role
    """
    if user.role == 1:
        redirect_url = "users:restaurant_dashboard"
        return redirect_url
    elif user.role == 2:
        redirect_url = "users:customer_dashboard"
        return redirect_url
    elif user.role is None and user.is_superuser:
        redirect_url = "/admin"
        return redirect_url


def send_verification_email(request, user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = "OnlineFood: Activate your account"
    message = render_to_string(
        "users/emails/email_verification.html",
        {
            "users": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": user_activation_token.make_token(user),
        },
    )
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context['users'].email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
