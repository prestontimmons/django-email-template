from functools import partial

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, RequestContext
from django.template.loader import get_template

from .util import render_node


def send_mail(template_name, context_data, send_method, render_method,
        request=None, from_email=None, **kwargs):

    kwargs["from_email"] = from_email or settings.DEFAULT_FROM_EMAIL

    kwargs.update(get_message(
        template_name=template_name,
        context_data=context_data,
        request=request,
        render_method=render_method,
    ))

    return send_method(**kwargs)


def get_message(template_name, context_data, request, render_method):
    if request:
        c = RequestContext(request, context_data)
    else:
        c = Context(context_data)

    template = get_template(template_name)
    return render_method(template, c)


def render_template(template, context):
    message = {}
    message["message"] = render_node(template, "text", context)
    message["subject"] = render_node(template, "subject", context)

    recipients = render_node(template, "recipients", context)
    recipient_list = []
    for recipient in recipients.split(","):
        recipient_list.append(recipient.strip())
    message["recipient_list"] = recipient_list

    return message


send = partial(send_mail,
    send_method=send_mail,
    render_method=render_template,
)
