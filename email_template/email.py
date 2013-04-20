from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, RequestContext
from django.template.loader import get_template

from .util import render_node


def send(template_name, context_data, request=None):
    message, subject, recipients = get_email_fields(
        template_name=template_name,
        context_data=context_data,
        request=request,
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
    )


def get_email_fields(template_name, context_data, request):
    if request:
        c = RequestContext(request, context_data)
    else:
        c = Context(context_data)

    template = get_template(template_name)
    message, subject, recipient_data = get_message(template, c)

    recipients = []
    for recipient in recipient_data.split(","):
        recipients.append(recipient.strip())

    return message, subject, recipients


def get_message(template, context):
    text = render_node(template, "text", context)
    subject = render_node(template, "subject", context)
    recipients = render_node(template, "recipients", context)
    return text, subject, recipients
