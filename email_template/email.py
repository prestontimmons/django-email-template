from functools import partial

from django.conf import settings
from django.core.mail import send_mail as send_django_mail
from django.template import Context, RequestContext
from django.template.loader import get_template

from .util import render_node


def send_base(template_name, context_data, send_method, render_method,
        request=None, from_email=None, send_method_args=None, **kwargs):

    send_method_args = send_method_args or {}

    args = get_message(
        template_name=template_name,
        context_data=context_data,
        request=request,
        render_method=render_method,
    )

    args["from_email"] = from_email or settings.DEFAULT_FROM_EMAIL
    args.update(send_method_args)

    return send_method(**args)

send_mail = send_base


def get_message(template_name, context_data, request, render_method):
    if request:
        c = RequestContext(request, context_data)
    else:
        c = Context(context_data)

    template = get_template(template_name)
    return render_method(template, c)


def render_django_fields(template, context):
    message = {}
    message["message"] = render_node(template, "text", context)
    message["subject"] = render_node(template, "subject", context)

    recipients = render_node(template, "recipients", context)
    recipient_list = []
    for recipient in recipients.split(","):
        recipient_list.append(recipient.strip())
    message["recipient_list"] = recipient_list

    return message


def send_django_wrapper(**kwargs):
    return send_django_mail(
        subject=kwargs["subject"],
        message=kwargs["message"],
        from_email=kwargs["from_email"],
        recipient_list=kwargs["recipient_list"],
    )


send_django = partial(send_base,
    send_method=send_django_wrapper,
    render_method=render_django_fields,
)
