from functools import partial

from django.template import Template
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import (
    setup_test_template_loader,
    restore_template_loaders,
)

from email_template.email import render_template, send_mail


EMAIL = Template("""
{% block subject %}Subject{% endblock %}
{% block text %}Hello from {{ name }}{% endblock %}
{% block recipients %}x@z.com, y@z.com{% endblock %}
""")

MISSING = Template("""
{% block recipients %}x@z.com, y@z.com{% endblock %}
""")


def send_method(**kwargs):
    return kwargs


send = partial(send_mail,
    send_method=send_method,
    render_method=render_template,
)


class SendMailTest(TestCase):

    def setUp(self):
        templates = {
            "email.html": EMAIL,
            "missing.html": MISSING,
        }
        setup_test_template_loader(templates)

    def tearDown(self):
        restore_template_loaders()

    def test_send(self):
        message = send(
            template_name="email.html",
            context_data=dict(name="Y"),
            request=None,
            from_email="x@y.com",
            send_method=send_method,
            header=2,
        )

        self.assertEqual(message["message"], "Hello from Y")
        self.assertEqual(message["subject"], "Subject")
        self.assertEqual(message["recipient_list"], ["x@z.com", "y@z.com"])
        self.assertEqual(message["from_email"], "x@y.com")
        self.assertEqual(message["header"], 2)

    def test_with_request(self):
        message = send(
            template_name="email.html",
            context_data=dict(name="Y"),
            request=RequestFactory().post("/email/"),
            send_method=send_method,
        )

        self.assertEqual(message["message"], "Hello from Y")
        self.assertEqual(message["subject"], "Subject")
        self.assertEqual(message["recipient_list"], ["x@z.com", "y@z.com"])

    def test_missing_subject_and_body(self):
        message = send(
            template_name="missing.html",
            context_data=dict(name="X"),
            request=RequestFactory().post("/email/"),
        )

        self.assertEqual(message["message"], "")
        self.assertEqual(message["subject"], "")
        self.assertEqual(message["recipient_list"], ["x@z.com", "y@z.com"])
