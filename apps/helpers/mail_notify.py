from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_reviewer_mail(to_email, context):
    subject = f"Thanks for your review on {context['review'].company.name}"
    template = 'email/reviewer.html'
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = to_email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def send_reviewed_mail(to_email, context):
    subject = f"Review on your business"
    template = 'email/reviewed.html'
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = to_email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def send_otp_mail(to_email, context):
    subject = "OTP Email"
    template = 'email/otp.html'
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = to_email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
