from functools import partial

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context, RequestContext
from django.template.loader import select_template

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

    if not isinstance(template_name, (list, tuple)):
        template_name = [template_name]

    template = select_template(template_name)
    return render_method(template, c)


def render_django_fields(template, context):
    message = {}
    message["text"] = render_node(template, "text", context)
    message["html"] = render_node(template, "html", context)
    message["subject"] = render_node(template, "subject", context)

    recipients = render_node(template, "recipients", context)
    recipient_list = []
    for recipient in recipients.split(","):
        recipient_list.append(recipient.strip())
    message["recipient_list"] = recipient_list

    return message


def send_django_wrapper(**kwargs):
    text = kwargs.get("text", "")
    html = kwargs.get("html", "")

    if text and html:
        email_class = EmailMultiAlternatives
    else:
        email_class = EmailMessage

    if html and not text:
        body = html
    else:
        body = text

    msg = email_class(
        subject=kwargs["subject"],
        body=body,
        from_email=kwargs["from_email"],
        to=kwargs["recipient_list"],
        headers=kwargs.get("headers", {}),
        cc=kwargs.get("cc", []),
    )

    if text and html:
        msg.attach_alternative(html, "text/html")

    if html and not text:
        msg.content_subtype = "html"

    msg.send()

    return msg


send_django = partial(send_base,
    send_method=send_django_wrapper,
    render_method=render_django_fields,
)
